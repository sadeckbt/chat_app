import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.utils import timezone

from chat.models import PrivateChat, Message


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'private_chat_{self.chat_id}'

        user = self.scope['user']
        chat, is_allowed = await self.get_chat_and_check_user(user)

        if user.is_anonymous or not is_allowed:
            await self.close()
        else:
            self.chat =chat
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')

        if message:
            msg_data = await self.save_message(self.scope["user"], message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': msg_data['content'],
                    'sender': msg_data['user'],
                    'timestamp': msg_data['sent_at'],
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_chat_and_check_user(self, user):
        try:
            chat = PrivateChat.objects.get(id=self.chat_id)
            return chat, user==chat.user1 or user==chat.user2
        except PrivateChat.DoesNotExist:
            return None, False

    @database_sync_to_async
    def save_message(self, user, content):
        message = Message.objects.create(
            user=user,
            content=content,
            private_chat_id=self.chat_id
        )
        return {
            'user': user.email,
            'content': message.content,
            'sent_at': str(timezone.localtime(message.sent_at)),
        }
