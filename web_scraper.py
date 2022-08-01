import requests 
from bs4 import BeautifulSoup
import csv
import re 

f = open('./test.csv', 'w')
writer = csv.writer(f, lineterminator = '\n')
writer.writerow(["Animal Name", "Scientific Name", "Status"])

# List of monotremes and marsupials of Australia WebScraper 

web_url = "https://en.wikipedia.org/wiki/List_of_monotremes_and_marsupials_of_Australia"

response = requests.get(
	url=web_url,
)

soup = BeautifulSoup(response.content, 'html.parser')

title = soup.find(id="bodyContent").find_all("li")



for tag in title:
    name = ""
    scientific_name = ""
    iucn_status = ""

    if("title=" in str(tag)):
        try:
            animal = str(tag).replace('"', '').split("title=")
            name = animal[1].split('>')[0]
            scientific_name = ((animal[1].split('<i>')[1])).split("<")[0]
            iucn_status = ((animal[2]).split(": ")[1]).split(">")[0]
            writer.writerow([name, scientific_name, iucn_status])
        except Exception as ex:
            print(ex)