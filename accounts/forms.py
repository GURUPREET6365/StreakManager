from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        
        # Add Bootstrap classes to all fields
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter old password'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name', 'password1', 'password2')
    

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
    