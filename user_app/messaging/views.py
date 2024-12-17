from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Message
from .forms import MessageForm, CustomUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()  # Use the custom user model

# User Registration View
def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use CustomUserCreationForm here
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'messaging/register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'messaging/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('user_login')

# Send Message View (User)
@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')

        try:
            receiver = User.objects.get(username=receiver_username)  # Find the receiver by username
        except User.DoesNotExist:
            return render(request, 'messaging/send_message.html', {'error': 'User not found'})

        # Create a new Message object and save it to the database (content is automatically encrypted by middleware)
        message = Message(sender=request.user, receiver=receiver, content=content)
        message.save()

        return redirect('user_dashboard')  # Redirect back to the user dashboard after sending the message

    return render(request, 'messaging/send_message.html')

