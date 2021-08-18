from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from first_app.forms import UserProfileInfoForm,UserForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def special(request):
    return HttpResponse('Вы вошли в аккаунт')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('first_app:index'))

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(request.method)
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('first_app:index'))
            else:
                return HttpResponse('Аккаунт не активен')
        else:
            print("Логин:{} и пароль {}".format(username,password))
            return HttpResponse("Неверные данные пользователя")
    else:
        return render(request,'first_app/login.html',{})

def index(request):
    return render(request,'first_app/index.html')

def register(request):
    registered=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)

            profile=profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()
            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'first_app/register.html',
                                                        {'userform':user_form,
                                                        'profileform':profile_form,
                                                        'registered':registered})
