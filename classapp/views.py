from django.shortcuts import render
def home_view(request):
	return render(request, "classapp/home.html")

def login_logout_view(request):
	return render(request, "classapp/login.html")

# def profile_card_view(request):
# 	return render(request, "classapp/")