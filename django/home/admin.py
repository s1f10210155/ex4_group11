from django.contrib import admin
from .models import Thread
from .models import Comment

# Register your models here.
admin.site.register(Thread)
admin.site.register(Comment)