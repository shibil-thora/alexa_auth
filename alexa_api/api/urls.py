from django.urls import path  
from . import views 
from oauth2_provider.views import AuthorizationView, TokenView

urlpatterns = [
    path('', views.HomeAPI.as_view(), name='home'),
    path('login/', views.user_login, name='login'), 
    path('userinfo/', views.UserInfoView.as_view(), name='userinfo'), 
    path('authorize/', AuthorizationView.as_view(), name='authorize'),
    path('token/', views.accessToken, name='tokendef'), 
    # path('toggle_bulb/', views.ToggleBulbAPI.as_view()),
    path("get_device_details",views.get_device_details),
]