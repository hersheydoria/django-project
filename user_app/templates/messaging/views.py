from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from .encryption_utils import encrypt_message, decrypt_message
from django.shortcuts import render
from .models import Message

from django.shortcuts import render

def user_dashboard(request):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None

    return render(request, 'messaging/dashboard.html', {'user_id': user_id})


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        encrypted_content = encrypt_message(data['content'])
        data['content'] = encrypted_content
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message sent securely'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReceiveMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user)
        for msg in messages:
            msg.content = decrypt_message(msg.content)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    