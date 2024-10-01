from django.shortcuts import render, redirect
from rest_framework.views import APIView 
from rest_framework.response import Response   
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import authenticate, login as auth_login 
import string 
import random 
import paho.mqtt.client as mqtt  
import os 
import json 
import time 
from django.views.decorators.csrf import csrf_exempt 
from .firebase import db, auth  
import secrets, hashlib 
from django.http import JsonResponse


BROKER = 'mqtt.onwords.in'  
PORT = 1883 
 
client = mqtt.Client() 
client.username_pw_set(os.environ.get('MQTT_USERNAME'), os.environ.get('MQTT_PASSWORD')) 


class HomeAPI(APIView): 
    def get(self, request): 
        return Response('hi')   
    
class GetToken(APIView):
    def post(self, request): 
        access_token = "access_shibil_123412"  
        refresh_token = "refresh_shibil_123412"  
        
        response_data = {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,  
            "refresh_token": refresh_token 
        }
        return Response(response_data)   
    

def generate_access_token(code):
    users_data = db.child("new_db").child("users").get().val()
    if not users_data:
        return "None"

    try:
        for uid, user_data in users_data.items():
            alexa_data = user_data.get("alexa", {})
            if alexa_data.get("authorization_code") == code:
                access_token_prefix = "Atza1|"
                characters = string.ascii_letters + string.digits
                random_part = ''.join(secrets.choice(characters) for _ in range(32))
                access_token = access_token_prefix + random_part
                db.child("new_db").child("users").child(uid).child("alexa").update({"access_token": access_token})
                return access_token

    except Exception as e:
        print(f"Error generating access token: {e}")
        return "None"

    return "None" 


def generate_access_token_login(refresh_token):
    users_data = db.child("new_db").child("users").get().val()
    if not users_data:
        return "None"

    try:
        for uid, user_data in users_data.items():
            alexa_data = user_data.get("alexa", {})
            if alexa_data.get("refresh_token") == refresh_token:
                access_token_prefix = "Atza1|"
                characters = string.ascii_letters + string.digits
                random_part = ''.join(secrets.choice(characters) for _ in range(32))
                access_token = access_token_prefix + random_part
                db.child("new_db").child("users").child(uid).child("alexa").update({"access_token": access_token})
                return access_token

    except Exception as e:
        print(f"Error generating access token with refresh token: {e}")
        return "None"

    return "None"


def refresh_access_token(code):
    users_data = db.child("new_db").child("users").get().val()
    if not users_data:
        return "None"

    try:
        for uid, user_data in users_data.items():
            alexa_data = user_data.get("alexa", {})
            if alexa_data.get("authorization_code") == code:
                access_token_prefix = "Atzr1|"
                characters = string.ascii_letters + string.digits
                random_part = ''.join(secrets.choice(characters) for _ in range(32))
                refresh_token = access_token_prefix + random_part
                db.child("new_db").child("users").child(uid).child("alexa").update({"refresh_token": refresh_token})
                return refresh_token

    except Exception as e:
        print(f"Error generating refresh token: {e}")
        return "None"

    return "None" 


def refresh_token_to_refresh(existing_refresh_token):
    users_data = db.child("new_db").child("users").get().val()
    if not users_data:
        return "None"

    try:
        for uid, user_data in users_data.items():
            alexa_data = user_data.get("alexa", {})
            if alexa_data.get("refresh_token") == existing_refresh_token:
                access_token_prefix = "Atzr1|"
                characters = string.ascii_letters + string.digits
                new_refresh_token = ''.join(secrets.choice(characters) for _ in range(32))
                db.child("new_db").child("users").child(uid).child("alexa").update({"refresh_token": new_refresh_token})
                return new_refresh_token

    except Exception as e:
        print(f"Error generating new refresh token: {e}")
        return "None"

    return "None"
    

@csrf_exempt
def accessToken(request):
    if request.method == 'POST':
        code = request.POST.get("code")
        refresh_token = request.POST.get("refresh_token")
        if refresh_token is not None:
            new_access_token = generate_access_token_login(refresh_token)
            new_refresh_token = refresh_token_to_refresh(refresh_token)
            return JsonResponse({"access_token": new_access_token, "token_type": "bearer", "expires_in": 86400, "refresh_token": new_refresh_token})

        elif code is not None:
            access_token = generate_access_token(code)
            refresh_token = refresh_access_token(code)
            return JsonResponse({"access_token": access_token, "token_type": "bearer", "expires_in": 86400, "refresh_token": refresh_token})
        else:
            return JsonResponse({"error": "Missing code or refresh_token"}, status=400)
    else:
        return JsonResponse({"error": "Unsupported request method"}, status=405)
    
    
class ToggleBulbAPI(APIView): 
    def post(self, request):  
        product_id = '4l2ftc005' 
        publish_topic = f'onwords/{product_id}/getCurrentStatus'
        subscribe_topic = f'onwords/{product_id}/currentStatus' 

        speech_output = ''

        def on_message(client, userdata, message):  
            print('got here....') 
            message_str = message.payload.decode()  
            message_dict = json.loads(message_str)
            print(message_dict['device1'], type(message_dict), 'type....') 
            change_status = 0 if message_dict['device1'] == 1 else 1
            device_1_dict = {}
            device_1_dict = {
                'device1': change_status,
                'id': product_id, 
                'client_id': 'akshay@onwords.in'
            } 
          
            message_string = json.dumps(device_1_dict)
            client.publish(publish_topic, message_string)
            print(f"Received message: {message_str} on topic: {message.topic}")  
            

        def on_connect(client, userdata, flags, rc): 
            client.subscribe(subscribe_topic) 
            request_data = {"request": "getCurrentStatus"}
            request_payload = json.dumps(request_data)
            client.publish(publish_topic, payload=request_payload, qos=1)
            print('MQTT connected!')

        client.connect(BROKER, PORT)  
        client.subscribe(subscribe_topic)
        client.on_connect = on_connect
        client.on_message = on_message  
        client.loop_start()

        response_data = {
            'text': 'action completed'
        }  

        time.sleep(0.3)
        client.loop_stop()
        client.disconnect()
        print('client disconnected')
        return Response(response_data)
    
def generate_authorization_code(uid, email, password):
    characters = string.ascii_letters + string.digits
    timestamp = str(int(time.time()))
    data_to_hash = f"{email}{password}{timestamp}"
    hashed_data = hashlib.sha256(data_to_hash.encode()).hexdigest()
    authorization_code = ''.join(secrets.choice(characters) for _ in range(16))
    try:
        db.child("new_db").child("users").child(uid).child("alexa").update({"authorization_code": authorization_code})
    except Exception as e:
        pass
    return authorization_code

@csrf_exempt
def user_login(request):  
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password') 
        user = None 
        try:
            user = auth.sign_in_with_email_and_password(email=email, password=password) 
            print(user, email, password)
        except:
            user = None
        print(user, email, password)
        if user is not None:  
            # try:
                state = request.GET.get('state') 
                uid = user['localId']
                redirect_uri = request.GET.get('redirect_uri')  
                authorization_code = generate_authorization_code(uid, email, password)
                return redirect(f'{redirect_uri}?code={authorization_code}&state={state}') 
            # except: 
            #     return render(request, 'login.html', {'error': 'Invalid state'})
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