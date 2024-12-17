# messaging/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  # Ensure the field names match your Message model