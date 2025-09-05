from django.db.models import Q
from rest_framework import serializers

from chat.models import PrivateChat, GroupChat, Message
from accounts.serializers import UserSerializer



class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'sent_at', 'is_read', 'private_chat', 'group_chat']


class PrivateChatSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    private_messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = PrivateChat
        fields = ['id', 'user1', 'user2', 'created_at', 'private_messages']

    def validate(self, attrs):
        user1 = self.context['request'].user
        user2 = attrs.get('user2')

        if user1 == user2:
            raise serializers.ValidationError(
                {'message': 'User can\'t chat with himself'}
            )

        existing_chat = PrivateChat.objects.filter(Q(user1=user1, user2=user2) or Q(user1=user2, user2=user1))
        if existing_chat.exists():
            raise serializers.ValidationError(
                {'message': 'Chat already exists'}
            )
        return attrs


class GroupChatSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    group_messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = GroupChat
        fields = ['id', 'name', 'users', 'created_at', 'group_messages']

