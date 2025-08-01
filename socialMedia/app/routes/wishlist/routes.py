from django.urls import path
from ...views.profile import Wishlist

urlpatterns=[
    path('save/', Wishlist.save, name='save'),
    path('wishlist/', Wishlist.wishlist, name='wishlist'),
    path('remove_wishlist/', Wishlist.remove_wishlist, name='remove_wishlist'),
]
