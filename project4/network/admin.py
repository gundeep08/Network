from django.contrib import admin
from .models import Post, Likes, Follow, Following, Messages


# Register your models here.
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Follow)
admin.site.register(Following)
admin.site.register(Messages)


