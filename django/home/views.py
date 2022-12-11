from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def pub_home(request):
    return render(request, "home/pub_home.html")

@login_required
def priv_home(request):
    return render(request, "home/priv_home.html")

@login_required
def search(request):
    return render(request, "home/search.html")