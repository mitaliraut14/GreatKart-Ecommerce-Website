from django.urls import path
from gkapp import views

urlpatterns = [
     path('',views.index),
     path('store',views.store),
     path('signin',views.signin),
     path('register',views.register),
     path('search_result',views.search_result),
     path('order_complete',views.order_complete),
     path('place_order',views.place_order),
     path('product_detail',views.product_detail),
     path('cart',views.cart),
     path('udash',views.dashboard),
     path('mobile_gen_otp',views.mobile_gen_otp),
     path('mobile_verf',views.mobile_verf),
     path('email_verf',views.email_verf),
     path('email_gen_otp',views.email_gen_otp),
     path('token',views.etoken_send),
     path('verify/<slug>',views.verify),
     path('error',views.error_page)
]