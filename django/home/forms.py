from django.forms import ModelForm
from .models import Thread
from .models import Comment

class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ("title", "content")

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)
