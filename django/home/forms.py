from django.forms import ModelForm
from .models import Thread, Comment, Room, CustomUser

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ("title", "content")

class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ("title", "content")

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)

class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password",)