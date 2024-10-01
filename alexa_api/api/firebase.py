import pyrebase
from os import environ

firebase_config = {
    "apiKey": environ.get('OST_API_KEY'),
    "authDomain": environ.get('OST_AUTH_DOMAIN'),
    "databaseURL": environ.get('OST_DATABASE_URL'),
    "projectId": environ.get('OST_PROJECT_ID'),
    "storageBucket": environ.get('OST_STORAGE_BUCKET'),
    "messagingSenderId": environ.get('OST_MESSAGING_SENDER_ID'),
    "appId": environ.get('OST_APP_ID'),
    "measurementId": environ.get('OST_MEASUREMENT_ID'),
}

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
