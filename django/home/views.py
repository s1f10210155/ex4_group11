from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "home/index.html")

def room(request, room_name):
    return render(request, "home/room.html", {"room_name": room_name})