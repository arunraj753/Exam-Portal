from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UserRegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. Enter valid email address.')
	class Meta(UserCreationForm.Meta):
		User = get_user_model()
		model=User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

        
