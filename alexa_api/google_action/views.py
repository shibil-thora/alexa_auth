from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response 
from .firebase import db


class HomeApi(APIView): 
    def get(self, request): 
        return Response('Home of google action') 
    

class ShyamApi(APIView): 
    def get(self, request, pk):  
        customer_data = db.child("customer").child(pk).get() 
        response_data = customer_data.val()
        return Response(response_data)