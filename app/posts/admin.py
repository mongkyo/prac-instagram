from django.contrib import admin

from .models import Post, HashTag, Comment

admin.site.register(Comment)
admin.site.register(HashTag)
admin.site.register(Post)