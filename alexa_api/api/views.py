from django.shortcuts import render, redirect
from rest_framework.views import APIView 
from rest_framework.response import Response   
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import authenticate, login as auth_login 
import string 
import random


class HomeAPI(APIView): 
    def get(self, request): 
        return Response('hi') 
    
def generate_authorization_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=30))

def user_login(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  
        if user is not None:  
            state = request.POST.get('state') 
            redirect_uri = request.POST.get('redirect_uri') 
            authorization_code = generate_authorization_code()
            auth_login(request, user)
            return redirect(f'{redirect_uri}?code={authorization_code}&state={state}')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })