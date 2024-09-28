from django.urls import path 
from . import views 

urlpatterns = [
    path('home/', views.HomeApi.as_view()),
    path('syam/<pk>', views.ShyamApi.as_view()),
]
