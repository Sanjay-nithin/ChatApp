from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        # Get or create user
        user, created = User.objects.get_or_create(username=username)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('chat')
    
    return render(request, 'chat/login.html')

@login_required
def chat_view(request):
    messages = Message.objects.all()[:50]  # Last 50 messages
    return render(request, 'chat/chat.html', {'messages': messages})
