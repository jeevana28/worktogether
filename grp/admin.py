from django.contrib import admin
from .models import Post, Comment, Message, Notification, FriendRequest
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(FriendRequest)
admin.site.register(Message)
admin.site.register(Notification)