from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Thread, Comment, Room, CustomUser
from .forms import ThreadForm, CommentForm, RoomForm, UserForm
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.db.models import Q
from functools import reduce
from operator import and_
from django.views import generic

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
    #ログインしているユーザーとidが一致したら,
    # そのユーザーがお気に入り登録しているroom_idを取り出し
    user = request.user.id
    rooms = Room.objects.filter(customuser=user).values().order_by("-created_datetime")
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

@login_required
def display_threads(request, room_id):
    rooms = Room.objects.filter(pk=room_id).values()
    room  = rooms[0]

    threads = Thread.objects.filter(room_id=room_id).values().order_by("-created_datetime")
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

#参考：https://zerofromlight.com/blogs/detail/59/#_4
@login_required
def search(request):
    room = Room.objects.order_by("-id")
    keyword = request.GET.get("keyword")
    if keyword:
        exclusion_list = set([' ', '　'])
        q_list = ''

        for i in keyword:
            if i in exclusion_list:
                pass
            else:
                q_list += i
        
        query = reduce(and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in q_list])

        room = room.filter(query)
        messages.success(request, "「{}」の検索結果".format(keyword))
    
    return render(request, "home/search_result.html", {"room": room})


#参考：https://qiita.com/checche/items/19bfd860770921427e29
def followRoom(request, room_id):
    place = get_object_or_404(Room, pk=room_id)
    request.user.favorite_room.add(place)
    return redirect('pub_home')

def create_user(request):
    if request.method == 'GET':
        form = UserForm
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            get_user_model().objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
        return redirect("pub_home")
    context = {
        'form': form
    }
    return render(request, "home/create_user.html", context)