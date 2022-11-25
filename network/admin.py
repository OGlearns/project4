from django.contrib import admin
from network.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserFollowing)
