from .models import verf_email
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
import datetime 
import razorpay
from greatkart.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY


# Create your views here.

def index(request):
    # if request.session.get('user_id'):
    #     userid=request.session['user_id']
        p=Product.objects.filter(status=1)
        content={}
        content['data']=p
        return render(request,'index.html',content)
    # else:
    #     return render(request,'index.html')

def store(request):
    return render(request,'store.html')

def signin(request):
    if request.method=="POST":
        email=request.POST['email']
        upass=request.POST['upass']
        usuccess={}
        u = authenticate(username=email, password=upass)
        print(u)
        # request.session['user_id'] = email
        if u is not None:
            login(request,u)
            # u=User.objects.get(username=u)
            # print(request.user.id)
            # lu=User.objects.get(username=u)
            # print(lu.id)
            # request.session['user.id']=u.id

            
            return redirect('/')

        else:
            usuccess['umsg']="User Not Registered!"
            return render(request,'signin.html',usuccess)    

    else:



        return render(request,'signin.html')

def register(request):
    if request.method=="POST":
        firstname=request.POST.get('fname')
        lastname=request.POST.get('lname')
        email=request.POST.get('email')
        password=request.POST.get('pass')
        confirmPassword=request.POST.get('cpass')
        error={}
        err=0
        success={}


            # if User.objects.filter(username = username).first():
            #     messages.success(request,'Username is taken.')
            #     return redirect ('/register')

            # if User.objects.filter(firstname = firstname).first():
            #     messages.success(request,'Firstname is taken.')
            #     return redirect ('/register')

            # if User.objects.filter(lastname = lastname).first():
            #     messages.success(request,'Firstname is taken.')
            #     return redirect ('/register')
            
        if firstname=="":
                err=1
                error['errfnamemsg']="First Name field cannot be Blank"
        if lastname=="":
                err=1
                error['errlnamemsg']="Last Name field cannot be Blank"
        elif email=="":
                err=1
                error['erremailmsg']="Username field cannot be Blank"
        elif password=="":
                err=1
                error['errpassmsg']="Password field cannot be Blank"
        elif confirmPassword=="":
                err=1
                error['errcupassmsg']="Confirm Password field cannot be Blank"
        elif password != confirmPassword:
                err=1
                error['errmismatch']="Password and confirm password didn't matched"
            
            # user_obj.save() data is save in database and profile_obj.save() data is save in django admin panel
        if err==0:
            u= User.objects.create_user(username = email,first_name=firstname,last_name=lastname,password=password)
            u.save()
            success['msg']="User Created Sucessfully!"
            
            return redirect('/email_gen_otp')
            # return render(request, "email_gen_otp.html", {'user':u})

        else:
            return render(request,'register.html',error)
    else:
         return render(request,'register.html')

def search_result(request):
    return render(request,'search_result.html')

def order_complete(request):
    return render(request,'order_complete.html')

def place_order(request,rid):
    if request.method=="POST":
        userid=request.user.id
        product = Product.objects.values().filter(id=rid)
        content={}
        content['data'] = product[0]
        print(product[0])
        print("logged in",userid)
        # print(request.method)
    
        # amount=request.POST.get(product[0]['price'])
        pin=request.POST.get('pincode')
        print(pin)
        # hou=request.POST.get('house')
        # build=request.POST.get('building')
        stre=request.POST.get('street')
        # state=request.POST.get('state')
        # add= hou + build + stre + state
        o=order.objects.create(uid = int(userid), pid = product[0]['id'], amount = product[0]['price'], placed_on = datetime.datetime.now(), pincode = pin, address = stre)
        o.save()
        print("what:", o)
    return render(request,'place_order.html',content)

def product_detail(request,rid):
    userid=request.user.id
    p=Product.objects.values().filter(id=rid)
    content={}
    content['data']=p
    # print(request.method)
    if request.method == "POST":
        print("logged in",userid)
      
        c=cart.objects.create(uid = int(userid), pid = p[0]['id'])
        c.save()
       
        print(c.pid)

    return render(request,'product_detail.html',content)

# def add_to_cart(request,rid):
#     userid=request.user.id
#     print("logged in",userid)
#     # c = cart.object.POST(uid= userid)   
#     # cart = request.session.get('cart', {})
#     product = Product.objects.values().filter(id=rid)
#     content={}
#     content['data'] = product
#     print(product[0])
#     c=cart.objects.create(uid = int(userid), pid = product[0]['id'])
#     c.save()
#     # c = cart.objects.create(pid = product, uid = userid)
#     # request.session['cart'] = cart
#     print(content)

#     return render(request,'add_to_cart.html')

def check_out(request,rrid):
    # if request.method=='POST':
        # print(rrid)
        #p=cart.objects.filter(uid=rrid)
        p=cart.objects.all()
        print(p)
        s=0
        product_id=str(p[0].pid.id)
        for i in range(1,len(p)):
            product_id=product_id+','+str(p[i].pid.id)
        
        print(product_id)
        for x in p:
            s=s+x.pid.price
           
    
        content={}
        content['data']=p
        content['tot']=s
        content['prod_id']=product_id
        return render(request,'check_out.html',content)


    # p=Product.objects.filter(id=rid)
    # print(product)
    # content={}
    # content['data']=product
    # return render(request,'product_detail.html')

def dashboard(request):
    return render(request,'dashboard.html')

def mobile_gen_otp(request):
    return render(request,'mobile_gen_otp.html')

def mobile_verf(request):
    return render(request,'mobile_verf.html')

def email_gen_otp(request):
    if request.method=="POST":
        email=request.POST.get('email')

        try:
            
            auth_token = random.randrange(1000,9999)
            profile_obj = verf_email.objects.create(email=email,em_otp = auth_token)
            profile_obj.save()
            send_mail_after_registation(email, auth_token)
            request.session['email'] = email
            return redirect('/email_verf')
            # return render(request, 'email_verf.html',{'email':email})

        except Exception as e:
            print(e)

    return render(request,'email_gen_otp.html')

def email_verf(request):
    # print(request.session['email'])

    # otp=request.POST.get('eotp')
    # em =request.session['email']

    # dbData = verf_email.objects.values_list("email", "em_otp").filter(email = em)
    # print(dbData[0][1])
    # print(otp)



    # print(dbData)
    print(request.method)
    if request.method=='POST':
        otp=request.POST.get('eotp')
        em =request.session['email']
        print(otp)
        dbData = verf_email.objects.values_list("email", "em_otp").filter(email = em)
        if(dbData[0][1] == int( otp)):

            return redirect('/signin')
        else:

            return render(request,'email_verf.html')
        # if(otp == dbData)

    #     # print("#################################", em , "##########", otp)
    else:

        return render(request,'email_verf.html')
    

def etoken_send(request):
    return render(request,'etoken_send.html')


def send_mail_after_registation(email,token):
    subject = 'Your account needs to be verified'
    # message = f'Hi paste the link to verify your accuont http://127.0.0.1:8000/email_verf/{token}'
    # otp=random.randrange(1000,9999)
    #to insert otp in database

    message=f'Enter {token} to verify your email'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list) 
    

def setsession(request):
    request.session['email']="sagarjaiswal7788@gmail.com"
    request.session['upass']="sagar"
    return render(request,'setsession.html')

def getsession(request):
    data={}
    data['semail']=request.session['email']
    data['pass']=request.session['upass']
    return render(request,'getsession.html',data)

def remove(request,rid):
    p=cart.objects.get(id=rid)#select * from blogapp_post where id=rid
    p.delete()
    return redirect('/')

client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
def pay(request):
    order_amount = 50000
    order_currency= 'INR'
    order_receipt= 'order_rcptid_11'
    note = {'Shipping address' : 'Pune, Maharashtra'}
    payment_order = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=note, payment_capture=1))
    payment_order_id = payment_order['id']
    content={ 'amount' : 500 , 'api_key' : RAZORPAY_API_KEY, 'order_id': payment_order_id }
    return render(request,'pay.html',content)