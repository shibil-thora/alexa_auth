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

BROKER = 'mqtt.onwords.in'  
PORT = 1883 
 
client = mqtt.Client() 
client.username_pw_set(os.environ.get('MQTT_USERNAME'), os.environ.get('MQTT_PASSWORD')) 


class HomeAPI(APIView): 
    def get(self, request): 
        return Response('hi')  
    
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
    
def generate_authorization_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=30))

@csrf_exempt
def user_login(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  
        if user is not None:  
            # try:
                state = request.POST.get('state') 
                redirect_uri = request.POST.get('redirect_uri')  
                print('state: ', state) 
                print(request.POST, 'post')
                print(request.GET, 'get')
                print('redirect_uri: ', redirect_uri)
                authorization_code = generate_authorization_code()
                auth_login(request, user)
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