from django.shortcuts import render
def home_view(request):
	return render(request, "classapp/home.html")

def login_view(request):
	return render(request, "classapp/login.html")