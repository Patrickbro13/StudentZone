from django.contrib import admin
from .models import Post, Contact, PostComment

admin.site.register(Post)
admin.site.register(Contact)
admin.site.register(PostComment)
