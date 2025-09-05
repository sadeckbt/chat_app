from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat.views import GroupChatViewSet, ListCreatePrivateChatView, get_private_messages, DeletePrivateChatView, list_group_users, list_group_online_users, get_group_messages

router = DefaultRouter()
#router.register('private-chats', PrivateChatViewSet, basename='privatechat')
router.register('group-chats', GroupChatViewSet, basename='group_chat')

urlpatterns = [
    path('', include(router.urls)),
    path('group-chats/<str:pk>/', get_group_messages),
    path('group-chats/<str:pk>/users/', list_group_users),
    path('group-chats/<str:pk>/users/online/', list_group_online_users),

    path('private-chats/', ListCreatePrivateChatView.as_view()),
    path('private-chats/<str:pk>/', get_private_messages),
    path('private-chats/<str:pk>/delete/', DeletePrivateChatView.as_view()),
]
