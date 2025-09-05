from django.urls import re_path
from chat.consumers.private import PrivateChatConsumer
from chat.consumers.group import GroupChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/private/(?P<chat_id>[0-9a-f-]+)/$', PrivateChatConsumer.as_asgi()),
    re_path(r'^ws/chat/group/(?P<chat_id>[0-9a-f-]+)/$', GroupChatConsumer.as_asgi()),
]
