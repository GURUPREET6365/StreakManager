from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
import os
from dotenv import load_dotenv

load_dotenv()

from .forms import CustomUserCreationForm, LoginForm
from .tokens import EmailVerificationTokenGenerator
from django.contrib.auth import get_user_model

User = get_user_model()

email_verification_token = EmailVerificationTokenGenerator()
# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = email_verification_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            domain = get_current_site(request).domain
            protocol = 'https' if request.is_secure() else 'http'
            verification_link = f"{protocol}://{domain}/verify-email/{uid}/{token}/"
            
            try:
                mail_subject = 'Verify your email address'
                message = render_to_string('accounts/email_verification.html', {
                    'user': user,
                    'activation_link': verification_link,
                })
                
                email_obj = EmailMessage(
                    subject=mail_subject,
                    body=message,
                    from_email=os.getenv('EMAIL_HOST_USER', 'quickprep001@gmail.com'),
                    to=[user.email]
                )
                email_obj.content_subtype = 'html'
                email_obj.send(fail_silently=False)  # ✅ Changed to False to see errors
                
                messages.success(request, f'Verification email sent to {user.email}. Check your inbox.')
                return redirect('login')
                
            except Exception as e:
                # Log the error for debugging
                print(f"Email send error: {e}")
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Email verification failed: {str(e)}")
                
                # Delete the user if email fails
                user.delete()
                messages.error(request, 'Failed to send verification email. Please try again.')
                return redirect('register')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def verify_email_view(request, uidb64, token):
    """
    Decode uidb64 to get user ID, check token, activate user
    """
    try:
        # Decode the encoded user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(f"DEBUG: uid type = {type(uid)}, uid value = {uid}")  
        uid = int(uid)
        print(f"DEBUG: uid after int() = {uid}")
        # Get the user
        user = User.objects.get(pk=uid)
        print(f"DEBUG: user found = {user.pk}")
        print(f'the type of the id is {type(user.pk)}')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Check if user exists and token is valid
    if user is not None and email_verification_token.check_token(user, token):
        # Activate the user
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Verification link is invalid or has expired.')
        user.delete()
        return redirect('register')
    

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            user = authenticate(request,
                                username=username,
                                password=password)
            if user is not None:
                #login(request, user): This function, also from django.contrib.auth, is crucial for establishing the user's session. It takes the request object and the authenticated user object as arguments. Its primary role is to set up the user's session in Django's authentication system, marking them as logged in. This includes storing the user's ID in the session, which allows Django to recognize the user on subsequent requests.
                messages.success(request, 'Logged in successful')
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials.')
                return redirect('login')
        else:
            return render(request, 'accounts/login.html', {'form':form,})
        
    return render(request, 'accounts/login.html', {
        'form':LoginForm,
    })


@login_required
def logout_view(request): 
    #logout(request) clears all session data for this request and removes the authentication state, and it is safe even if the user was not logged in
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')



@login_required
def delete_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.info(request, 'Account deleted.')
        return redirect('home')
    else:
        messages.error(request, 'An error occured.')

@login_required
def profile(request):
    # user_id = User.objects.filter(user_id=request.user)
    # The request.user object already contains the logged-in user's data
    current_user = request.user

    user={'username':current_user.username,
            'f_name':current_user.first_name,
            'l_name':current_user.last_name,
            'email':current_user.email,       
            'l_login':current_user.last_login,
            'date_joined':current_user.date_joined,          
        }
    
    return render(request, 'accounts/profile.html', {'user':user,})