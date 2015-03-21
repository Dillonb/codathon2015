from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from classapp.models import *

def home_view(request):
	return render(request, "classapp/home.html")

def logout_view(request):
    logout(request)
    return render(request, "classapp/loggedout.html")

@login_required
def course_list_view(request):
    courses = request.user.course_set.all()
    return render(request,"classapp/courselist.html",{"courses": courses})


# def profile_card_view(request):
# 	return render(request, "classapp/")
