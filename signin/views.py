from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'login/login.html')

def account(request):
    return render(request, 'account/account.html')