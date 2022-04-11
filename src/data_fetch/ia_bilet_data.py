from asyncio.windows_events import NULL
from calendar import month
from cgitb import text
from contextlib import nullcontext
from http.client import ImproperConnectionState
import json
import time
import copy
from turtle import update
from selenium import webdriver
from selenium.webdriver.common.by import By
MAIN_LINK ="https://www.iabilet.ro"
TEST_FILE = "verificare.txt"
PATH = "src\drivers\chromedriver2.exe"

def data_dumping(data):
   f = open(TEST_FILE,'a')
   f.write(data)
   f.close()
   

def get_event_description(driver,id):
    new_driver =  webdriver.Chrome(PATH)
    next_link = driver.find_element(by = By.XPATH, value = ".//a[contains(@href,'" +str(id) + "')]").get_attribute("href")
    new_driver.get(next_link)
    t = new_driver.find_element(by=By.CLASS_NAME, value = "main-content")
    x = t.find_element(by=By.CLASS_NAME, value = "short-desc").text
    x = x.replace("Mai multe detalii", "")
    new_driver.quit()
    return x


def update_event(all_events,event,i):
    all_events["events"][i]["data"]["description"]= event["data"]["description"]
    all_events["events"][i]["data"]["event_location"] = event["data"]["event_location"]
    return all_events

def page_scraper(driver,all_events,event_types):
    search = driver.find_element(by =By.ID,value ="eventListPaginatedId")
    events = search.find_elements(by = By.CLASS_NAME , value ="row")  
    add_to_list = True
    #more_data = driver.find_element_by_id("btn-more-container text-center")
    for t  in events:
        
        #extracting the id of the event
        text_length = t.get_dom_attribute("data-likable-item")
        text_length = text_length.replace("event/","")
        id = int(text_length)
        event = {"id" : id, "data": {}}

        #adding the event Types
        event["event_types"] = event_types
        #extracting the dates
        date_start =  t.find_element(by= By.CLASS_NAME, value = "date-start")
        date_start_day =  date_start.find_element(by= By.CLASS_NAME, value = "date-day").text
        date_start_month =  date_start.find_element(by= By.CLASS_NAME, value = "date-month").text
        event["data"]["date_start_day"] =  int(date_start_day)
        event["data"]["date_start_month"] = date_start_month
        #print(date_start_day+ date_start_month)
        try:
            date_end =  t.find_element(by= By.CLASS_NAME, value = "date-end")
        except:
            date_end = NULL

        date_end_day = NULL
        date_end_month = NULL
        if( date_end  != NULL ):
            
            date_end_day = date_end.find_element(by= By.CLASS_NAME, value = "date-day").text
            date_end_month = date_end.find_element(by= By.CLASS_NAME, value = "date-month").text
            event["data"]["date_end_day"] = int(date_end_day)
            event["data"]["date_end_month"] = date_end_month

        #extracting the event name
        event_name = t.find_element(by= By.CLASS_NAME, value = "title").text
        event["data"]["event_name"] = event_name
        #print(event_name)

        #extracting the event name
        event_location = t.find_element(by= By.CLASS_NAME, value = "location").text
        event["data"]["event_location"] = event_location
        #de spart in 2 locatie exacta + oras
        #print(event_location)

        #extracting  event description WIP

        event["data"]["description"] = get_event_description(driver,id)

        #adding event Types
        event["event_types"] = event_types

        #extracting event price
        try: 
            event_price = t.find_element(by= By.CLASS_NAME, value = "price").text
            event["data"]["event_price"] = event_price
        except:
            event_price = NULL
        for i,t in enumerate(all_events["events"]):
            if t["id"] == event["id"]:
                all_events = update_event(all_events,event,i)
                add_to_list = False
                break
        if add_to_list:
            all_events["events"].append(event)
            add_to_list = True

        
    try:
        n = search.find_element(by= By.CLASS_NAME, value = "btn-more-container")
        next_page = n.find_element(by= By.CLASS_NAME, value = "btn")
        next_page_link = next_page.get_dom_attribute("href")
        next_page_link = MAIN_LINK + next_page_link
        driver.get(next_page_link)
        #data_dumping({"sunt la pagina" : inc})
        #data_dumping(all_events)
        page_scraper(driver,all_events,event_types)

    except:
        print("am terminat cu link-ul asta")
    return all_events


def add_to_event_types(event_types, values):
    for value in values:
        if value in event_types:
            continue
        else:
            event_types.append(value)
    return event_types

def ia_bilet_data(driver,all_events):
    event_types = []
    link_and_e_t ={}
    all_links = []
    #search = driver.find_element(by = By.CLASS_NAME, value =  "user-contextual-menu")
    concerts = driver.find_elements(by= By.XPATH, value = '/html/body/header/div[3]/div/div/ul[1]/li[3]/div/ul/li/a')
    concerts = concerts[:len(concerts)-2]
    for x in concerts:

        link_and_e_t["event_type"] = ["Concert ",(x.get_attribute('innerHTML'))]

        next_page_link = x.get_dom_attribute("href")
        if MAIN_LINK in next_page_link:
            link_and_e_t["link"] = next_page_link
        else: 
            next_page_link =MAIN_LINK + next_page_link
            link_and_e_t["link"] = next_page_link
        #print(link_and_e_t)
        all_links .append(copy.copy(link_and_e_t))
            
    for i in range(4,5):
        #print(str(i) + " PIZDAAAAAAA")
        
        limits = driver.find_elements(by= By.XPATH, value = '/html/body/header/div[3]/div/div/ul[1]/li["' + str(i) + '"]/div/a')
        limits  = limits [3:]
        i = 3
        for x in limits:
            event_types = []
            #new_driver = copy.copy(driver)
            next_page_link = x.get_dom_attribute("href")
            next_page_link =MAIN_LINK + next_page_link
            #print(next_page_link)
            link_and_e_t["link"] = next_page_link
            link_and_e_t["event_type"]= [(x.text)]
            #print(event_types)
            #driver.get(next_page_link)
            #all_events = page_scraper(new_driver,all_events,event_types)
            #print(link_and_e_t)
            all_links.append(copy.copy(link_and_e_t))
            i = i + 1

    for x  in all_links:
        #print(x["link"])
        #print(x["event_type"])
        event_types = add_to_event_types(event_types, x["event_type"])
        driver.get(x["link"])
        all_events = page_scraper(driver,all_events,x["event_type"])
           
    return event_types, all_events

    
#/html/body/header/div[3]/div/div/ul[1]/li[3]/div/ul/li[1]/a
#/html/body/header/div[3]/div/div/ul[1]/li[4]/div/a
#/html/body/header/div[3]/div/div/ul[1]/li[9]/div/a
#/html/body/header/div[3]/div/div/ul[1]/li[3]/div/ul/li[1]/a
#/html/body/header/div[3]/div/div/ul[1]/li[3]/div/ul/li[1]/a#


#//*[@id="eventListPaginatedId"]/div[1]/div[1]/div[1]/a
#//*[@id="eventListPaginatedId"]/div[1]/div[2]/div[1]/a
#//*[@id="eventListPaginatedId"]/div/div[1]/div[1]/a
#//*[@id="eventListPaginatedId"]/div/div[1]/div[1]/a
#//*[@id="eventListPaginatedId"]/div[1]/div[1]/div[1]/a