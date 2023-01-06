from django.contrib import admin
from .models import Thread, Comment, Room

# Register your models here.
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(Room)