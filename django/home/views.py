from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Thread
from .forms import ThreadForm
from django.contrib.auth.models import User

# Create your views here.
def pub_home(request):
    form = ThreadForm
    context = {
        "form": form,
    }
    return render(request, "home/pub_home.html", context)

@login_required
def priv_home(request):
    return render(request, "home/priv_home.html")

@login_required
def search(request):
    return render(request, "home/search.html")

@login_required
def create_room(request):
    form = ThreadForm(request.POST)
    context = {
        "form": form,
    }
    if form.is_valid():
        thread = form.save(commit=False)
        thread.user = request.user
        thread.save()
    return render(request, "home/create_room.html", context)