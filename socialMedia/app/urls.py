from django.urls import path, include
from .routes.auth import routes as auth_routes
from .routes.main import routes as main_routes
from .routes.wishlist import routes as wishlist_routes


urlpatterns = [
    path('auth/', include(auth_routes)),
    path('main/', include(main_routes)),
    path('wishlist/', include(wishlist_routes))

]