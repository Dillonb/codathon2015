from django.shortcuts import render
from django.contrib.auth import logout

def home_view(request):
	return render(request, "classapp/home.html")

def logout_view(request):
    logout(request)

# def profile_card_view(request):
# 	return render(request, "classapp/")
