from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Thread, Comment, Room
from .forms import ThreadForm, CommentForm, RoomForm
from django.contrib.auth.models import User

# Create your views here.
def pub_home(request):
    return render(request, "home/pub_home.html")

@login_required
def create_room_page(request):
    form = RoomForm
    context = {
        "form": form,
    }
    return render(request, "home/create_room_page.html", context)

def display_rooms(request):
    rooms = Room.objects.all().values()
    count = len(rooms)
    for count in range(count):
        username_dicts = User.objects.filter(pk=rooms[count]["user_id"]).values("username")
        rooms[count].update(username_dicts[0])

    #form = RoomForm

    paginator = Paginator(rooms, 8)
    current_page = request.GET.get("current_page")
    rooms = paginator.get_page(current_page)
    context = {
        "rooms": rooms,
        #"form": form,
    }
    return render(request, "home/display_rooms.html", context)

@login_required
def create_room(request):
    form = RoomForm(request.POST)
    if form.is_valid():
        room = form.save(commit=False)
        room.user = request.user
        room.save()
    return redirect("pub_home")

def display_threads(request, room_id):
    rooms = Room.objects.filter(pk=room_id).values()
    room  = rooms[0]

    threads = Thread.objects.filter(room_id=room_id).values()
    count = len(threads)
    for count in range(count):
        username_dicts = User.objects.filter(pk=threads[count]["user_id"]).values("username")
        threads[count].update(username_dicts[0])

    form = ThreadForm

    paginator = Paginator(threads, 8)
    current_page = request.GET.get("current_page")
    threads = paginator.get_page(current_page)
    context = {
        "room": room,
        "threads": threads,
        "form": form,
    }
    return render(request, "home/display_threads.html", context)

@login_required
def create_thread(request):
    room_id = request.POST['room_id']
    form = ThreadForm(request.POST)
    if form.is_valid():
        newthread = form.save(commit=False)
        newthread.user = request.user
        newthread.room_id = room_id
        newthread.save()
    return redirect('display_threads', room_id = room_id)

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
    return redirect('display_comments', thread_id = thread_id)

@login_required
def priv_home(request):
    return render(request, "home/priv_home.html")

@login_required
def search(request):
    return render(request, "home/search.html")
