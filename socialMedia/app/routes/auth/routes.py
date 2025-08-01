from django.urls import path
from ...views.auth import LoginView
from ...views.auth import RegisterView
from ...views.auth import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.RegisterView, name='register'),
    path('login/', LoginView.LoginView, name='login'),
    path('logout_view/', LogoutView.logout_view, name='logout_view'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]   
