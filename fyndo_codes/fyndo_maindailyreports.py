import json
import copy
import sys
sys.path.append('/Library/Python/2.7/site-packages')
import requests
import datetime
import time

resp = requests.get('http://fyndox.herokuapp.com/api/selectFeeds')
feedmain = resp.json()

data = []

print('The total number of feeds is - ' + str(len(feedmain)))

for i in range(len(feedmain)):
    if feedmain[i]['feedId'] >= 2279:
        data.append(feedmain[i])

print('The total number of feeds after 2279 is - ' + str(len(data)))

def feedsreport():
    startdate = input('Enter start date - ')
    enddate = input('Enter end date - ')
    month = input('Enter month - ')
    cats = []
    areas = []
    feeds = []
    arealist = []
    results = {}
    latlong = []
    
    for i in range(len(data)):
        acttime=[]
        if data[i]['dateOfPost'] is None:
            h = 0

        else:
            x=1
            timestamp = data[i]['dateOfPost']
            timestamp = int(timestamp)/1000
            acttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))[0:10].split('-')
            if int(acttime[1]) == int(month) and int(acttime[2]) >= int(startdate) and int(acttime[2]) <= int(enddate):
                cats.append(data[i]['userCatLevel1'])
                areaf = str(data[i]['shopArea'])           
                arlt = areaf.split(', ')
                if int(len(arlt))>2:
                    for j in range(len(arlt)):
                        if str(arlt[j].lower()) == 'Chennai'.lower():
                            x=j
                    arealist.append(arlt[x-1])
                    data[i]['newArea'] = str(arlt[x-1])
                    feeds.append(data[i])
    
    cats = list(set(cats))
    arealist = list(set(arealist))
    
    #print('The number of feeds in the give date range - ' + str(len(feeds)))
    #print('The categories are - ')
    #for i in range(len(cats)):
    #    print(cats[i])
    #print('The areas are - ')
    #for i in range(len(arealist)):
    #    print(arealist[i])

    for i in range(len(arealist)):
        results[arealist[i]] = dict((k,0) for k in cats)
        results[arealist[i]]['total'] = 0

    #print(results)
    print('\n\nThe total numbers of feeds for the selected date period is - ' + str(len(feeds)) + '\n\n' + 'Results below - \n')
    
    for i in range(len(feeds)):
        results[feeds[i]['newArea']]['total'] = results[feeds[i]['newArea']]['total'] + 1
        results[feeds[i]['newArea']][feeds[i]['userCatLevel1']] = results[feeds[i]['newArea']][feeds[i]['userCatLevel1']] + 1
        ll = []
        ll.append(feeds[i]['gpsLatitude'])
        ll.append(feeds[i]['gpsLongitude'])
        latlong.append(ll)

    for keys in results:
        print('Area - ' + str(keys) + ' - ' + str(results[keys]['total']))
        for keys1 in results[keys]:
            if keys1 != 'total':
                print(str(keys1) + ' - ' + str(results[keys][keys1]))
        print('\n\n')
    print('The lat longs are - ' + str(len(latlong)))
    for t in range(len(latlong)):
        print(str(latlong[t][0]) +',' + str(latlong[t][1]))
#def bizcovered():
    

    
    
        
    
    
