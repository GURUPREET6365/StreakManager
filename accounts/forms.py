
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Form for change password
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type':'password', 
        'class':'form-control',
        'id':'oldpassword', 
        'name':'oldpassword',
        'placeholder':'Old Password',
        'required':True
    }))
    new_password1 = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={
        'type':'password', 
        'class':'form-control',
        'id':'newpassword1', 
        'name':'newpassword1',
        'placeholder':'New Password',
        'required':True
    }))
    new_password2 = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={
        'type':'password', 
        'class':'form-control',
        'id':'newpassword2', 
        'name':'newpassword2',
        'placeholder':'Confirm New Password',
        'required':True
    }))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder':'Enter First Name',
                'class':'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder':'Enter Last Name',
                'class':'form-control',
            }),
            'username': forms.TextInput(attrs={
                'placeholder':'Enter Username',
                'class':'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder':'Enter Email',
                'class':'form-control',
            }),
        }

    # FIX PASSWORD FIELDS HERE
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Enter Password',
            'id':'id_password1'
        })

        self.fields['password2'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Confirm Password',
            'id':'id_password2'
        })


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(attrs={
        'class':'form-control', # It is the bootstrap desigining method.
        'placeholder':'Enter your username',
        'required':True,
        'autofocus':True,
        

    }))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={
        'class':'form-control', # It is the bootstrap desigining method.
        'placeholder':'Enter your password',
        'required':True,
        'autofocus':True,
        'type':'password',
        'id':'id_password1'
    }), label='Password')
    

class ChangeUsername(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',     # Bootstrap class
                'placeholder': 'Enter new username',
            })
        }

class ChangeFnameLname(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',     # Bootstrap class
                'placeholder': 'Enter first name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',     # Bootstrap class
                'placeholder': 'Enter first name',
            })
        }

class ChangeEmail(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Enter New Email',
                'id':'email',
                'name':'email',
                'type':'email'
            })
        }