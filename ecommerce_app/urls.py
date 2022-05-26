
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/<slug:product_slug>/',
        views.show_product, name='product_detail'),
    path('cart/', views.show_cart, name='show_cart'),
    path('checkout/', views.checkout, name='checkout'),
path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),


    path('about-page/',views.about,name='about'),
    path('product-page/', views.product, name='product'),
    path('schedule-page/', views.schedule, name='schedule'),
    path('donation-page/', views.donation, name='donation'),
    path('speakers-page/', views.speakers, name='speakers'),
    path('founder-page/', views.founder, name='founder'),
    path('purchaseticket-page/', views.purchase_tickets, name='purchaseticket'),

]