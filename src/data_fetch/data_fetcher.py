from http.client import ImproperConnectionState
import json
from operator import truediv
import os
from pickle import TRUE
from selenium import webdriver
import copy

from data_fetch.ia_bilet_data import ia_bilet_data
PATH = "src\drivers\chromedriver.exe"
SITES_PATH = "D:\Event_App\src\data\sites.txt"
JSON_EVENTS = "src\data\events.json"
JSON_EVENT_TYPES = "src\data\event_types.json"



def data_fetcher():
    all_events = {"events": []}
    all_event_types = {"event_types": []}
    event_type ={}
    sites= []
    with open(SITES_PATH) as f:
        sites = f.readlines()
    print(sites[0])
    driver = webdriver.Chrome(PATH)
    if( os.stat(JSON_EVENTS).st_size != 0):
        with open(JSON_EVENTS,encoding="utf-16") as outfile:
            all_events = json.load(outfile,)
            outfile.close()
    if( os.stat(JSON_EVENT_TYPES).st_size != 0):
        with open(JSON_EVENT_TYPES,encoding="utf-16") as outfile:
            all_event_types = json.load(outfile)
            outfile.close()
    driver.get(sites[0])
    new_event_types = []
    new_event_types, all_events = ia_bilet_data(driver, all_events)
    all_events["events"] = sorted(all_events["events"], key= lambda id: id['id'])


    no_of_e_t = len(all_event_types["event_types"])
    id = all_event_types["event_types"][no_of_e_t-1]["id"] + 1
    print(id)
    for value in new_event_types:
        new_val = True
        for x in all_event_types["event_types"]:
            if x["event_type"] == value:
                new_val = False
                break
        if new_val:
            event_type["id"] = id
            event_type["event_type"] = value
            all_event_types["event_types"].append(copy.copy(event_type))
            id = id + 1

    #print(all_event_types)
    #print(len(all_events["events"]))

    json_data = json.dumps(all_events, ensure_ascii= False)
    with open(JSON_EVENTS, "w", encoding="utf-16") as outfile:
        outfile.write(json_data)

    json_data = json.dumps(all_event_types,ensure_ascii= False)
    with open(JSON_EVENT_TYPES, "w", encoding="utf-16") as outfile:
        outfile.write(json_data)
    driver.quit()
    