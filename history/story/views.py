from django.shortcuts import render, get_object_or_404, redirect
from .models import Story
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError



def home(request):
    return render(request, 'story/home.html')


def story(request):
    story = Story.objects.order_by('date')
    return render(request, 'story/story.html', {'story': story})


def detail(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    return render(request, 'story/detail.html', {'story': story})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'story/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('story')
            except IntegrityError:
                return render(request, 'story/signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'Такое имя пользователя уже существует!'})
        else:
            return render(request, 'story/signupuser.html',
                          {'form': UserCreationForm(),
                           'error': 'Пароли не совпали'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'story/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'story/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Неверные данные для входа'})
        else:
            login(request, user)
            return redirect('story')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')