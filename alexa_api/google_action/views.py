from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response


class HomeApi(APIView): 
    def get(self, request): 
        return Response('Home of google action')