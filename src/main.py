import json
import os
import time
from data_fetch.data_fetcher import data_fetcher
from data_imports import JSON_EVENT_TYPES
from fb.firebase_con import firebase_con

def main():
    duration = time.time()
    data_fetcher()
    firebase_con()
    duration = time.time() - duration
    print("executia a durat " + str(int(duration)) + " secunde")

if __name__ == "__main__":
    main()
