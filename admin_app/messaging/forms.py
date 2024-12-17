# messaging/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  # Ensure the field names match your Message model