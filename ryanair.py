import json
import requests
from datetime import datetime

datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')


def cheapFlightsFrom (origin,outboundStart,outboundEnd):
    url='https://api.ryanair.com/farefinder/3/oneWayFares?&departureAirportIataCode='+origin+'&language=en&limit=1000&market=en-gb&offset=0&outboundDepartureDateFrom='+outboundStart+'&outboundDepartureDateTo='+outboundEnd
    result =requests.get(url).text
    j=json.loads(result)
    fares=[]
    for v in j['fares']:
        price=v['outbound']['price']['value']
        destination=v['outbound']['arrivalAirport']['iataCode']
        depDate=v['outbound']['departureDate']
        arrDate=v['outbound']['arrivalDate']
        fares.append([price, origin,  destination, depDate, arrDate])
    return fares

firstAP='STN'
startDateStr='2017-03-15'
lastAP='STN'
finishDate='2017-03-31'

startDate=datetime.strptime(startDateStr,"%Y-%m-%d")
finishDate=datetime.strptime(startDateStr,"%Y-%m-%d")

fares=cheapFlightsFrom(firstAP,startDateStr,startDateStr)
print(fares)
