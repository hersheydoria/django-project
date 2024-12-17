from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, MessageForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from .encryption_utils import encrypt_message, decrypt_message
from django.http import JsonResponse
from cryptography.fernet import InvalidToken
from django.contrib.auth import get_user_model

User = get_user_model()  # Use the custom user model

# Admin Registration View
def admin_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'messaging/register.html', {'form': form})

# Admin Dashboard View
@login_required
def admin_dashboard(request):
    users = User.objects.exclude(id=request.user.id)
    messages = Message.objects.filter(receiver=request.user)

    # Decrypt the message content before displaying it
    for message in messages:
        message.content = message.get_decrypted_content()

    return render(request, "messaging/dashboard.html", {"users": users, "messages": messages})

# Admin Login View
def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'messaging/login.html', {'form': form})

# Admin Logout View
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Send Message View
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

        return redirect('admin_dashboard')  # Redirect back to the user dashboard after sending the message

    return render(request, 'messaging/send_message.html')

# Message List View
def message_list(request):
    messages = Message.objects.all()
    return JsonResponse({'messages': [message.to_dict() for message in messages]})

# Secure API Endpoint for Sending Messages
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
