from django.contrib import admin
from .models import Thread, Comment, Room, CustomUser, UserManager

# Register your models here.
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(Room)
admin.site.register(CustomUser)
#admin.site.register(UserManager)