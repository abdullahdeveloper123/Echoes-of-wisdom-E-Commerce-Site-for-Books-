
from ...views.profile import Orders
from ...views.books import main
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', main.home, name='home'),
    path('home/', main.home, name='home'),
    path('details/<int:id>', main.detail, name='details'),
    path('search/', main.search, name='search'),
    path('create-payment-intent/', Orders.create_payment_intent, name='create_payment_intent'),
    path('save_order/', Orders.save_order, name='save_order'),
    path('get_orders/', Orders.get_orders, name='get_orders'), 
    path('library/', main.library, name='library'), 
    path('add_books/', main.add_books, name='add_books'), 

    
]   