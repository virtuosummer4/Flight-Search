import json
import requests
import csv


origin='STN'
outboundStart='2017-03-01'
outboundEnd='2017-03-05'
url='https://api.ryanair.com/aggregate/3/common?embedded=airports,countries,cities,regions,nearbyAirports,defaultAirport&market=en-gb'

result =requests.get(url).text
j=json.loads(result)

print(j['airports'][0].keys())

ap=[]
for v in j['airports']:
    name=v['name']
    code=v['iataCode']
    region=v['regionCode']
    lat=v['coordinates']['latitude']
    lon=v['coordinates']['longitude']
    ap.append([name,code,region,lat,lon])

for v in ap:
    print(v)
