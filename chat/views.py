from rest_framework import permissions
from rest_framework import viewsets, generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from accounts.models import User

from chat.models import PrivateChat, GroupChat
from chat.serializers import GroupChatSerializer, PrivateChatSerializer, UserSerializer


# Create your views here.
class GroupChatViewSet(viewsets.ModelViewSet):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GroupChat.objects.filter(users=self.request.user)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        user_ids = request.data.get('user_ids', [])

        if not name:
            return Response({'error': 'Group name is required.'}, status=400)

        group = GroupChat.objects.create(name=name)
        group.users.add(request.user, *User.objects.filter(id__in=user_ids))
        serializer = self.get_serializer(group)
        return Response(serializer.data, status=201)


@api_view(['GET'])
def list_group_users(request, pk):
    chat_group = GroupChat.objects.filter(id=pk).first()
    if not chat_group:
        return Response(
            {'message': 'Chat group not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GroupChatSerializer(chat_group)
    return Response(
        {
            'message': 'Users',
            'data': serializer.data['users']
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def list_group_online_users(request, pk):
    chat_group = GroupChat.objects.filter(id=pk).first()
    if not chat_group:
        return Response(
            {'message': 'Chat group not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    online_users = chat_group.users.filter(is_online=True)
    serializer = UserSerializer(online_users, many=True)
    return Response(
        {
            'message': 'Users',
            'data': serializer.data
        }
    )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_group_messages(request, pk):
    user = request.user
    group = GroupChat.objects.filter(id=pk).first()
    if not group:
        return Response(
            {'message': 'Group not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not (user in group.users or user.is_staff):
        return Response(
            {'message': 'You are not member of this group'},
            status=status.HTTP_403_FORBIDDEN
        )
    serializer = GroupChatSerializer(group)
    return Response(
        {
            'message': 'Group message',
            'data': serializer.data
        },
        status=status.HTTP_200_OK
    )



class ListCreatePrivateChatView(generics.ListCreateAPIView):
    queryset = PrivateChat.objects.all()
    serializer_class = PrivateChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrivateChat.objects.all()

    def list(self, request, *args, **kwargs):
        return PrivateChat.objects.filter(user1=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user1=self.request.user)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_private_messages(request, pk):
    user = request.user
    chat = PrivateChat.objects.filter(id=pk).first()
    if not chat:
        return Response(
            {'message': 'Chat not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    if not (user == chat.user1 or user == chat.user2 or user.is_staff):
        return Response(
            {'message': 'You are not member of this chat'},
            status=status.HTTP_403_FORBIDDEN
        )
    serializer = PrivateChatSerializer(chat)
    return Response(
        {
            'message': 'Messages',
            'data': serializer.data
        },
        status=status.HTTP_200_OK
    )



class DeletePrivateChatView(generics.DestroyAPIView):
    queryset = PrivateChat.objects.all()
    serializer_class = PrivateChatSerializer
    lookup_field = 'pk'

    def get_object(self):
        chat = super().get_object()
        user = self.request.user
        if not (user==chat.user1 or user==chat.user2 or user.is_staff):
            raise PermissionDenied(
                {'message': 'You are not allowed to delete this chat'}
            )
        return chat
