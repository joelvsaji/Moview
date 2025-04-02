from django.shortcuts import render,redirect
from .forms import*
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect("moviewapp:home")
    # if they are not logged in
    else:
        if request.method=="POST":
            form=RegistreationForm(request.POST or None)
            if form.is_valid():
                user=form.save()
                raw_password=form.cleaned_data.get('password1')
                user=authenticate(username=user.username,password=raw_password)
                login(request,user)
                return redirect("moviewapp:home")
        else:
            form=RegistreationForm()
        return render(request,'register.html',{"form":form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect("moviewapp:home")
    else:
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("moviewapp:home")
                else:
                    return render(request,'login.html',{"error":"Your account has been diasbled."})
            else:
                return render(request,'login.html',{"error":"Invalid Username or Password. Try Again."})
        return render(request,'login.html')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("accounts:login")
    else:
        return redirect("accounts:login")