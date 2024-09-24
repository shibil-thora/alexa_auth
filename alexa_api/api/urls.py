from django.urls import path  
from . import views 
from oauth2_provider.views import AuthorizationView, TokenView

urlpatterns = [
    path('', views.HomeAPI.as_view(), name='home'),
    path('login/', views.user_login, name='login'), 
    path('userinfo/', views.UserInfoView.as_view(), name='userinfo'), 
    path('authorize/', AuthorizationView.as_view(), name='authorize'),
    path('token/', TokenView.as_view(), name='token'),
]
