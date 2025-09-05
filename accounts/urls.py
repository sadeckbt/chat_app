from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('activation/', views.account_activation, name='activation'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('user/', views.user_detail, name='user'),

    path('delete/', views.delete_account, name='delete_account'),

    path('refresh', views.refresh_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]