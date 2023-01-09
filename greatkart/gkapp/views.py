from .models import Profile
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

def index(request):
    return render(request,'index.html')

def store(request):
    return render(request,'store.html')

def signin(request):
    return render(request,'signin.html')

def register(request):
    return render(request,'register.html')

def search_result(request):
    return render(request,'search_result.html')

def order_complete(request):
    return render(request,'order_complete.html')

def place_order(request):
    return render(request,'place_order.html')

def product_detail(request):
    return render(request,'product_detail.html')

def cart(request):
    return render(request,'cart.html')

def dashboard(request):
    return render(request,'dashboard.html')

def mobile_gen_otp(request):
    return render(request,'mobile_gen_otp.html')

def mobile_verf(request):
    return render(request,'mobile_verf.html')

def email_gen_otp(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:

            if User.objects.filter(username = username).first():
                messages.success(request,'Username is taken.')
                return redirect ('/register')

            if User.objects.filter(email = email).first():
                messages.success(request,'Email is taken.')
                return redirect ('/register')

            user_obj = User(username = username, email  = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registation(email, auth_token)

            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request,'email_gen_otp.html')

def email_verf(request):
    return render(request,'email_verf.html')

def etoken_send(request):
    return render(request,'etoken_send.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'YOur account has been verified.')
            return redirect('/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def error_page(request):
    return render(request, 'error.html')


def send_mail_after_registation(email,token):
    subject = 'Your account needs to be verified'
    message = f'Hi paste the link to verify your accuont http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list) 
