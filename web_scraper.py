import requests 
from bs4 import BeautifulSoup
import csv
import re 

f = open('./test.csv', 'w')
writer = csv.writer(f, lineterminator = '\n')
writer.writerow(["Animal Name", "Scientific Name", "Status, Ibra, Eco Descriptors"])

# List of monotremes and marsupials of Australia WebScraper 
web_url = "https://en.wikipedia.org/wiki/List_of_monotremes_and_marsupials_of_Australia"
# Database of Australian animals
gov_db = "https://biodiversity.org.au/afd/taxa/"


# Initially scrape the wikipedia page 
response = requests.get(
	url=web_url,
)

soup = BeautifulSoup(response.content, 'html.parser')
title = soup.find(id="bodyContent").find_all("li")


# Scrape the government webpage to find more details 
def get_eco_details(scientific_name):
    IBRA = ""
    eco_descriptors = "" 
    try:
        response = requests.get(
            url=gov_db+scientific_name.replace(" ", "_"),
            )
        if(response.status_code != 200):
            response = requests.get(
                url=gov_db+scientific_name.replace(" ", "_")+";"+scientific_name.split(" ")[0]
                )           
            if(response.status_code != 200):
                response = requests.get(
                url=gov_db+scientific_name.replace(" ", "_").replace('(', '').split(')')[0]
                )   
                if(response.status_code != 200):
                    raise Exception("No animal found")

        soup = BeautifulSoup(response.content, 'html.parser')

        ibra_flag = False 

        for data in (soup.find(id='afdDistribution')): 
            if(data.text == "IBRA"):
                ibra_flag = True
                continue
            if(data.text != "" and data.text != None and ibra_flag == True ):
                if((re.search(r"\bACT\b|\bNSW\b|\bQld\b|\bSA\b|\bTas\b|\bVic\b|\bWA\b|\bNT\b", str(data)) != None)):
                    IBRA = (" ".join(str(data.text).split())) 
                    break 
        # backup checker
        if(IBRA == ""):
            for data in (soup.find(id='afdDistribution')): 
                if((re.search(r"\bACT\b|\bNSW\b|\bQld\b|\bSA\b|\bTas\b|\bVic\b|\bWA\b|\bNT\b", str(data)) != None)):
                    IBRA = (" ".join(str(data.text).split())) 
                    break 
                
            
        eco_descriptors = ((soup.find(id='afdEcologicalDescriptors').findAll('p'))[0]).text
    except: 
        pass  
    
    return IBRA, eco_descriptors
        
        

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
            IBRA = "" 
            eco_descriptors = "" 
            
            IBRA, eco_descriptors = get_eco_details(scientific_name)
            
            writer.writerow([name, scientific_name, iucn_status, IBRA, eco_descriptors])
        except Exception as ex:
            print(ex)