#!/usr/bin/env python3
import csv
import json
import re
import io
import requests

def getBestFlights(origin, date):
    API_KEY = "ha135592433329469511355786664317"
    
    browse_quotes = "http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/GB/GBP/en-GB/"+origin+"/anywhere/"+date+"/?apiKey={}"
    
    result = json.loads(requests.get(browse_quotes.format(API_KEY)).text)
    #print("QUOTES")
    #print(json.dumps(result, indent=4))
    
    goodresults = []
    for i, item in enumerate(result['Routes']):
        if "Price" in item.keys():
            price = item["Price"]
            quotes = item["QuoteIds"]
            goodresults.append([price, quotes])
            
    goodresults.sort()
    
    bestresults = []
    for item in goodresults:
        price = item[0]
        quotenum = item[1][0]
        myquote = result['Quotes'][quotenum-1]
        if not myquote['Direct']:
            continue
        try:
            carrier = myquote['OutboundLeg']['CarrierIds'][0]
            for item2 in result['Carriers']:
                if item2['CarrierId'] == carrier:
                    carriername = item2['Name']
        except IndexError:
            carriername = None
        destination = myquote['OutboundLeg']['DestinationId']
        for item2 in result['Places']:
            if item2['PlaceId'] == destination:
                destinationname = item2['Name']
        bestresults.append([price, carriername, destinationname])
        
    return bestresults








def checkCity(ufrom, file):
    #city - string with
    #file - csv table Airport,Country,IATA,ICAO
    file.seek(0)
    readr = csv.DictReader(file)
    i=0
    for row in readr:
        #print(str(i))
        #print(str(row))
        i=i+1
        if(ufrom.lower()==row["IATA"].lower()):
        #if(ufrom==row["Airport"] or ufrom==row["City"] or ufrom==row["Country"] or ufrom==row["IATA"]):
            return row["Airport"]
    return ""
    
    
airp_file = open("euAirports.csv")


print("Good day to you, adventurous traveler.")
print("What great places places you shall discover?\n")
done = False


#print("Hello\nWorld")
homeairp=[]
homenam = []
urfrom = input('Which airport would you like to fly from? (IATA code, please)')

while ~done:
    print(urfrom)
    frCity=checkCity(urfrom, airp_file)
    print(frCity)
    if frCity!="":
        homeairp.append(urfrom)
        homenam.append(frCity)
        print(frCity+"- got it.")
        ans = input("Anywhere else? (y/n)")
        if ans.lower() == "y" or ans.lower() =="yes":
            urfrom = input("Where?")
        else:
            done = True
            break
    else:
        urfrom = input("We couldn't recognise the name. Could you rephrase that please?")
        
print("You are flying from")
for i in range(0, len(homeairp)):
    print(homenam[i])

prog = re.compile("^\d{4}-\d{2}-\d{2}$")

dtime = input("When are you leaving? (yyyy-mm-dd)")
while prog.match(dtime)=="":
    dtime = input("Could you rephrase that please? (yyyy-mm-dd)")
print(dtime + ", got it.\n Give me a sec.")

bf=[]
for i in range(0, len(homeairp)):
    bf.append(getBestFlights(homeairp[i].upper(), dtime))
print("Your cheap flights are:\n")

for i in range(0, len(bf)):
    print("\n")
    print("From "+homeairp[i]+" " + homenam[i])
    flights = bf[i]
    for  j in range(0, len(flights)):
        print("To "+flights[j][2] + " via " + flights[j][1] + " for " + str(flights[j][0]) + " pounds")
    
    
