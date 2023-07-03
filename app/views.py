from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def register(request):
    UFO=UserForm()
    PFO=ProfileForm()
    d={'ufo':UFO, 'pfo':PFO}

    if request.method=='POST' and request.FILES:
        UO=UserForm(request.POST)
        PO=ProfileForm(request.POST,request.FILES)

        if UO.is_valid() and PO.is_valid():
            USUO=UO.save(commit=False)
            USUO.set_password=UO.cleaned_data['password']
            USUO.save()

            USPO=PO.save(commit=False)
            USPO.username=USUO
            USPO.save()

            send_mail('Registration',
                      'Registraion is successful',
                      'darevenky424@gmail.com',
                      [USUO.email],
                      fail_silently=False

            )

            return HttpResponse('Registration is successfull')
        else:
            return HttpResponse('not valid data')

    return render(request,'register.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password') 
        
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def change_password(request):
    if request.method=='POST':
        password=request.POST['password']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(password)
        UO.save()
        return HttpResponse('password changed successfully')

    return render(request,'change_password.html')


def reset_password(request):

    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        LUO=User.objects.filter(username=username)
        #UO=LUO[0]
        if LUO:
            LUO[0].set_password(password)
            LUO[0].save()
            return HttpResponse('password is successfully changed')
        else:
            return HttpResponse('Username is not vailable')
        
    return render(request,'reset_password.html')
