from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Message
from .forms import MessageForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

User = get_user_model()  # Use the custom user model

def home(request):
    return render(request, 'messaging/home.html') 

def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')  # Redirect to the user dashboard after update
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'user_dashboard.html', {'form': form})

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

from django.contrib import messages

# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:  # Check if the user is an admin (superuser)
                return redirect('user_dashboard')  # Redirect admins to the admin dashboard or other page
            login(request, user)
            return redirect('user_dashboard')  # Redirect regular users to the user dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'messaging/login.html', {'form': form})


# User Logout View
def user_logout(request):
    logout(request)
    return redirect('user_login')

# User Dashboard View
@login_required
def user_dashboard(request):
    # Fetch users that the logged-in user has communicated with (either as sender or receiver)
    sent_messages = Message.objects.filter(sender=request.user).values('receiver')
    received_messages = Message.objects.filter(receiver=request.user).values('sender')

    # Extract user IDs from the dictionaries and create sets of user IDs
    sent_user_ids = {message['receiver'] for message in sent_messages}
    received_user_ids = {message['sender'] for message in received_messages}

    # Combine the user IDs to get a unique set of communicated user IDs
    communicated_user_ids = sent_user_ids | received_user_ids

    # Fetch the actual user objects for these user IDs
    communicated_users = User.objects.filter(id__in=communicated_user_ids)

    # Fetch the user's messages (both sent and received)
    messages = Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user)

    # Decrypt the message content before displaying it
    for message in messages:
        message.content = message.get_decrypted_content()

    return render(request, "messaging/dashboard.html", {
        "users": communicated_users,
        "messages": messages
    })

# Send Message View (User)
@login_required
def send_message(request, user_id=None):
    # If user_id is provided, display previous messages and a form to send a new message
    if user_id:
        try:
            receiver = User.objects.get(id=user_id)
            messages = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
            messages = messages.order_by('-timestamp')  # Sort by most recent first

            # Decrypt the message content before displaying it
            for message in messages:
                message.content = message.get_decrypted_content()

        except User.DoesNotExist:
            return redirect('user_dashboard')  # If the user doesn't exist, go back to the dashboard

        # Handle POST request to send a new message
        if request.method == 'POST':
            content = request.POST.get('content')
            if content:
                message = Message(sender=request.user, receiver=receiver, content=content)
                message.save()
                return redirect('send_message_with_user', user_id=user_id)  # Redirect to the same page to display the new message

        return render(request, 'messaging/send_message_with_user.html', {'receiver': receiver, 'messages': messages})

    # If no user_id is provided, show a form to send a message to any user
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')
        try:
            receiver = User.objects.get(username=receiver_username)
            message = Message(sender=request.user, receiver=receiver, content=content)
            message.save()
            return redirect('user_dashboard')  # Redirect to the dashboard after sending the message
        except User.DoesNotExist:
            return render(request, 'messaging/send_message.html', {'error': 'User not found'})

    return render(request, 'messaging/send_message.html')

# Secure API Endpoint for Sending Messages (User)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import MessageSerializer

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response({'message': 'Message sent securely'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Secure API Endpoint for Receiving Messages (User)
class ReceiveMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)