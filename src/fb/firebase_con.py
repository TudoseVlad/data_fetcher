import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from data_imports import FIREBASE_CREDENTIALS, JSON_EVENT_TYPES, JSON_EVENTS


def upload_to_fs(json_path,db):
    if( os.stat(json_path).st_size != 0):
        with open(json_path,encoding="utf-16") as outfile:
            lista = json.load(outfile)
            outfile.close()
    #print(lista)
    for key,lista in lista.items():
        doc_ref = db.document('Data/' + key).set({key : lista})
def firebase_con():
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)
    print("works")
    db = firestore.client()
    upload_to_fs(JSON_EVENT_TYPES,db)
    upload_to_fs(JSON_EVENTS,db)
    
    