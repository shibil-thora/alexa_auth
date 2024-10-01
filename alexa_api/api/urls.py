from django.urls import path  
from . import views 
from oauth2_provider.views import AuthorizationView, TokenView

urlpatterns = [
    path('', views.HomeAPI.as_view(), name='home'),
    path('toggle_bulb/', views.ToggleBulbAPI.as_view()), 
    path("", views.home),
    path("login/", views.login),
    path("login-auth/", views.loginAuth),
    path("access-token/", views.accessToken),
    path("get_device_details/",views.get_device_details),
    path("success/", lambda request: views.HttpResponse("Token exchange successful!")),
]
