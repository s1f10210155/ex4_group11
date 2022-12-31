from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Thread, Comment
from .forms import ThreadForm, CommentForm
from django.contrib.auth.models import User

# Create your views here.
def pub_home(request):
    return render(request, "home/pub_home.html")

def display_threads(request):
    threads = Thread.objects.all().values()
    count = len(threads)
    for count in range(count):
        username_dicts = User.objects.filter(pk=threads[count]["user_id"]).values("username")
        threads[count].update(username_dicts[0])

    form = ThreadForm

    paginator = Paginator(threads, 12)
    current_page = request.GET.get("current_page")
    threads = paginator.get_page(current_page)
    context = {
        "threads": threads,
        "form": form,
    }
    return render(request, "home/display_threads.html", context)

@login_required
def create_room(request):
    form = ThreadForm
    context = {
        "form": form,
    }
    return render(request, "home/create_room.html", context)

@login_required
def create_thread(request):
    form = ThreadForm(request.POST)
    if form.is_valid():
        thread = form.save(commit=False)
        thread.user = request.user
        thread.save()
    return redirect("pub_home")

@login_required
def display_comments(request, thread_id):

    threads = Thread.objects.filter(pk=thread_id).values()
    thread  = threads[0]
    username_dicts = User.objects.filter(pk=threads[0]['user_id']).values('username')
    thread.update(username_dicts[0])

    comments = Comment.objects.filter(thread_id=thread_id).values()
    count = len(comments)

    for count in range(count):
        username_dicts = User.objects.filter(pk=comments[count]['user_id']).values('username')
        comments[count].update(username_dicts[0])

    form = CommentForm
    context = {
        'thread': thread,
        'comments': comments,
        'form': form,
    }
    return render(request, 'home/display_comments.html', context)

@login_required
def create_comment(request):
    thread_id = request.POST['thread_id']

    form = CommentForm(request.POST)

    if form.is_valid():

        comment = form.save(commit=False)

        comment.user = request.user
        comment.thread_id = thread_id

        comment.save()
    return redirect('home:display_comments', thread_id = thread_id)

@login_required
def priv_home(request):
    return render(request, "home/priv_home.html")

@login_required
def search(request):
    return render(request, "home/search.html")
