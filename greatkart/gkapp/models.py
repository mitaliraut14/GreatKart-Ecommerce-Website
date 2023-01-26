from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):

    product_name=models.CharField(max_length=100)
    pdesc=models.CharField(max_length=500)
    price=models.IntegerField()
    image=models.ImageField()
    created_at=models.DateTimeField()
    status=models.IntegerField()

class cart(models.Model):

    uid=models.IntegerField()
    pid=models.ForeignKey(Product, on_delete=models.CASCADE)

class order(models.Model):

    pid=models.CharField(max_length=100)
    uid=models.IntegerField()
    amount=models.IntegerField()
    placed_on=models.DateTimeField()
    pincode=models.IntegerField()
    address=models.CharField(max_length=500)
    

class orderpayment(models.Model):
    razor_pay_order_id=models.CharField(max_length=100 , null=True , blank = True)
    razor_pay_payment_id=models.CharField(max_length=100 , null=True , blank = True)
    razor_pay_payment_signature=models.CharField(max_length=100 , null=True , blank = True)

class verf_mobile(models.Model):

    mob_otp=models.IntegerField()

class verf_email(models.Model):

    email=models.CharField(max_length=100)
    em_otp=models.IntegerField()

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
