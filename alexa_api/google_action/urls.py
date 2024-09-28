from django.urls import path 
from . import views 

urlpatterns = [
    path('home/', views.HomeApi.as_view()),
    path('shyam/<id>', views.ShyamApi.as_view()),
]
