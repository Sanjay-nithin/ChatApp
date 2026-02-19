from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message
import json

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

@login_required
@csrf_exempt
def upload_voice(request):
    if request.method == 'POST' and request.FILES.get('voice'):
        voice_file = request.FILES['voice']
        message = Message.objects.create(
            user=request.user,
            message_type='voice',
            voice_note=voice_file
        )
        return JsonResponse({
            'success': True,
            'voice_url': message.voice_note.url,
            'message_id': message.id
        })
    return JsonResponse({'success': False}, status=400)
