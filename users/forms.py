from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from users.models import Profile

class RegistrationForm(UserCreationForm):
    phone   	=forms.CharField(max_length=10,help_text='Required,Enter a valid Phone Number')
    email 		=forms.EmailField(help_text='Required, Enter a valid email.')
    first_name	=forms.CharField(max_length=60,help_text='Enter first name')
    last_name	=forms.CharField(max_length=60,help_text='Enter Last name')

    class Meta:
        model = User
        fields = ['phone','email','first_name','last_name','password1','password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['phone', 'email','first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 'image']
