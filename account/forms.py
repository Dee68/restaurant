from django.forms import widgets
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )

    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'address', 'gender', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class':'form-control','placeholder': 'Write something about yourself...'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'your address here.'}),
            'gender': forms.Select(attrs={'class':'form-control','placeholder': 'Gender'}, choices=GENDER),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'upload your avatar'})
         }