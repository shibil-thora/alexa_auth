import pyrebase
from os import environ

firebase_config = {
    "apiKey": environ.get('API_KEY'),
    "authDomain": environ.get('AUTH_DOMAIN'),
    "databaseURL": environ.get('DATABASE_URL'),
    "projectId": environ.get('PROJECT_ID'),
    "storageBucket": environ.get('STORAGE_BUCKET'),
    "messagingSenderId": environ.get('MESSAGING_SENDER_ID'),
    "appId": environ.get('APP_ID'),
    "measurementId": environ.get('MEASUREMENT_ID'),
}

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
