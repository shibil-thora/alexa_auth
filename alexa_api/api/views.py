from django.shortcuts import render, redirect
from rest_framework.views import APIView 
from rest_framework.response import Response   
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import authenticate, login as auth_login


class HomeAPI(APIView): 
    def get(self, request): 
        return Response('hi') 
    

def user_login(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  
        print(user, username, password, 'here')
        if user is not None: 
            print(user, 'coming here')
            auth_login(request, user)
            return redirect('home')
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