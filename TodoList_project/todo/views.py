from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.utils import timezone
from .form import todoForm
from .models import Todo
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':     #if someone types signup in url
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    else:
            #create new user
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodo')
            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Username is already taken"})
        else:
            #Tell user password didn't match
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Your password didn't match"})

def loginuser(request):
    if request.method == 'GET':     #if someone types signup in url
        return render(request,'todo/login.html',{'form':AuthenticationForm()})
    else:
            #login user
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user != None:
            login(request, user)
            return redirect('currenttodo')
        else:
            #Tell user password didn't match username
            return render(request,'todo/login.html',{'form':AuthenticationForm(),'error':"Your password didn't match username"})

@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method=='GET':
        return render(request, 'todo/createtodo.html', {'form': todoForm()})
    else:
        try:
            form= todoForm(request.POST)
            newtodo= form.save(commit=False)
            newtodo.user=request.user
            newtodo.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': todoForm(),'error':'Bad data passed in.Try again'})

@login_required
def currenttodo(request):
    todos= Todo.objects.filter(user=request.user,dateCompleted__isnull=True)
    return render(request,'todo/curenttodo.html',{'todos':todos})

@login_required
def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk,user=request.user)
    if request.method == 'GET':
        form= todoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo,'form':form})
    else:
        try:
            form= todoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo,'form': form,'error':'Bad data passed in.Try again'})

@login_required
def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk,user=request.user)
    if request.method=='POST':
        todo.dateCompleted=timezone.now()
        todo.save()
        return redirect('currenttodo')

@login_required
def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodo')

@login_required
def completedlist(request):
    todos= Todo.objects.filter(user=request.user,dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request,'todo/completedlist.html',{'todos':todos})
