import json
import time
from data_fetch.data_fetcher import data_fetcher
from fb.firebase_con import firebase_con
JSON = "test.json"
def main():
    duration = time.time()
    data_fetcher()
    #firebase_con()
    duration = time.time() - duration
    print("executia a durat " + str(int(duration)) + " secunde")

main()
