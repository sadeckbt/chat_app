from django.contrib import admin

from .models import PrivateChat, GroupChat, Message


# Register your models here.
admin.site.register(PrivateChat)
admin.site.register(GroupChat)
admin.site.register(Message)
