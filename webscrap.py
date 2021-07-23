import bs4 
import urllib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import pandas as pd
import csv

df = open('hellostudent_data.csv')
content = csv.reader(df)
prev_price=[]
for row in content:
    if(row[6] !=  ' Price(Per week per person)'):
       prev_price.append(row[6])

i = 0
page_url = "https://www.hellostudent.co.uk/locations/"

output_file_name = "hellostudent_data.csv"
headers = "City Name, Property name, Room type, Duration of stay, Start date, Availability(Number of beds), Price(Per week per person), Previous price(Per week per person) \n"

# opens file, and writes headers
f = open(output_file_name, "w")
f.write(headers)


uClient = uReq(page_url)
page_html = uClient.read()

page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div", {"class": "collage__item"})

for container in containers:   
    city_name = container.section.h1.text
    a_tag = container.findAll("a", {"class":"btn"})
    url1 = a_tag[0]["href"]

    uClient1 = uReq(url1)
    page_html1 = uClient1.read()

    page_soup1 = soup(page_html1, "html.parser")

    containers1 = page_soup1.findAll("div", {"class": "card-group__item"})

    for item in containers1: 
        link_container = item.findAll("a", {"class": "btn"})
        discover_link = link_container[0]["href"]
        name_container =item.findAll("h4", {"class": "heading heading--gamma heading--near"})
        name_of_property = name_container[0].text 
        #print("Name of property is " + name_of_property + " and it's link is " + discover_link)

        uClient2 = uReq(discover_link)
        page_html2 =  uClient2.read()
        page_soup2 = soup(page_html2, "html.parser")

        containers2 = page_soup2.findAll("table", {"class": "table"})
        try:
            t_body = containers2[0].tbody
        except:
            continue
        rooms = t_body.findChildren('tr') 
        for room in rooms:
            stats = room.findChildren('td')
            room_type = ""
            price = ""
            duration = ""
            start = ""
            availability = ""
            available=""
            for stat in stats:
                try:
                    if stat["data-prefix"] == "Room Type":
                        room_type = stat.h4.text 
                    if stat["data-prefix"] == "Price":
                        price = stat.text 
                    if stat["data-prefix"] == "Weeks":
                        duration = stat.text 
                    if stat["data-prefix"] == "Start Date":
                        start = stat.strong.text 
                except:
                    if stat["class"] == ['table__cell', 'table__cell--upper', 'table__cell--accent']:
                        available = stat["data-info"]
                        availability = available[15:]
            print("City name is " + city_name)
            print("Name of property is " + name_of_property)
            print("Room type is " + room_type.strip())
            print("The price per week per person is " + price.strip())
            print("The duration of stay is " + duration.strip() + "days.") 
            print("Start date is " + start.strip())
            print("The availabilty of beds right now is " + availability.strip() + " beds.") 
            f.write(city_name + ", " + name_of_property + ", " + room_type.strip() + ", " + duration.strip() + ", " + start.strip() + ", " + availability.strip() + ", " + price.strip() + ", " + prev_price[i] + "\n")
            i = i + 1
            print("********************")

        print("----------xxxxxx---------------xxxx------------xxx------------------xxx-----------------------xxx---------------------------------")
    print("----------------------xxxxx-----------------------------CITY CHANGE------------------------------xxxxx--------------------------------")





