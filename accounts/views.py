from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login,authenticate
from .form import SignUpForm
from django.core.exceptions import SuspiciousOperation
from django.contrib import messages

# Create your views here.


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('home_qg')
    return render(request,'signup.html',{'form':form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                return redirect('home_qg')
            else:
                raise SuspiciousOperation('please enter a correct username and password')
        else:
            messages.warning(request, 'please enter a correct username and password')
    return render (request, 'login.html')


