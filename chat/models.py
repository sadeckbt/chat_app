import uuid

from django.db import models
from accounts.models import User


# Create your models here.
class GroupChat(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(User, related_name='group_chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class PrivateChat(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user1.email} -- {self.user2.email}'



class Message(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    private_chat = models.ForeignKey(PrivateChat, null=True, blank=True, on_delete=models.CASCADE, related_name='private_messages')
    group_chat = models.ForeignKey(GroupChat, null=True, blank=True, on_delete=models.CASCADE, related_name='group_messages')

    def __str__(self):
        return self.content
