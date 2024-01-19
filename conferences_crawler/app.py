import firebase_admin
from firebase_admin import credentials




class app:
    def __init__(self):
        cred = credentials.Certificate("./conferences-crawler-firebase-adminsdk-181yi-4cbb903707.json")
        firebase_app = firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://conferences-crawler-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
