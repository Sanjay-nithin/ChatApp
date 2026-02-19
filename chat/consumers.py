import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_room'
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'text')
        username = data['username']

        if message_type == 'text':
            message = data['message']
            # Save message to database
            await self.save_message(username, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'message_type': 'text'
                }
            )
        elif message_type == 'voice':
            voice_url = data['voice_url']
            # Send voice message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'voice_url': voice_url,
                    'username': username,
                    'message_type': 'voice'
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message_type = event.get('message_type', 'text')
        username = event['username']

        if message_type == 'text':
            message = event['message']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'username': username,
                'message_type': 'text'
            }))
        elif message_type == 'voice':
            voice_url = event['voice_url']
            # Send voice message to WebSocket
            await self.send(text_data=json.dumps({
                'voice_url': voice_url,
                'username': username,
                'message_type': 'voice'
            }))

    @database_sync_to_async
    def save_message(self, username, message):
        user = User.objects.get(username=username)
        Message.objects.create(user=user, content=message)
