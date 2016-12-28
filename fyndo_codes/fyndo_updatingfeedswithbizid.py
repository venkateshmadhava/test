import json
import copy
import sys
sys.path.append('/Library/Python/2.7/site-packages')
import requests
import geopy
from geopy.distance import vincenty


urlbiz = 'http://fyndo.herokuapp.com/api/selectBizInfos'
bizresp = requests.get(urlbiz)
biz = bizresp.json()

bdic = {}

for y in range(len(biz)):
    bdic[biz[y]['bizId']] = biz[y]['bizName']


urlfeed = 'http://fyndox.herokuapp.com/api/selectFeeds'
feedresp = requests.get(urlfeed)
feedsmain = feedresp.json()

urlupdate = 'http://fyndox.herokuapp.com/api/updateFeed'


def feedsupdate():
    x = input('Enter starting feeds id: ')
    y = input('Enter ending feed id: ')
    notupdatedfeeds = []
    feeds = []
    for i in range(len(feedsmain)):
        if int(feedsmain[i]['feedId']) >= int(x) and int(feedsmain[i]['feedId']) <= int(y):
            feeds.append(feedsmain[i])

    for i in range(len(feeds)):
        d = {}
        t=0
        results = {}
        
        if feeds[i]['shopName'] != "":
            
            for j in range(len(biz)):
                feedshop = []
                bizshop = []
                fscore = 0.0000
                bscore = 0.0000
                fdltlg = (feeds[i]['gpsLatitude'],feeds[i]['gpsLongitude'])
                bzltlg = (biz[j]['gpsLatitude'],biz[j]['gpsLongitude'])
                
                if feeds[i]['shopName'] is None:
                    feedshop = []
                else:
                    feedshop = feeds[i]['shopName'].lower().split(" ")
                    
                if biz[j]['bizName'] is None:
                    bizshop = []
                else:
                    bizshop = biz[j]['bizName'].lower().split(" ")
                    
                try:
                    feedshop.remove('')
                    feedshop.remove(' ')
                    bizshop.remove('')
                    bizshop.remove(' ')
                    
                except:
                    mmmm = 0
               
                for k in range(len(feedshop)):
                    if feedshop[k] in bizshop:
                        fscore = fscore + 1
                        
                for p in range(len(bizshop)):
                    if bizshop[p] in feedshop:
                        bscore = bscore + 1

                if len(feedshop) == 0:
                    fscore = 0.0000
                else:
                    fscore = fscore/int(len(feedshop))

                if len(bizshop) == 0:
                    bscore = 0.0000
                else:
                    bscore= bscore/int(len(bizshop))
                
                if fscore > 0.5 or bscore > 0.5 and int(vincenty(fdltlg,bzltlg).meters)<=25:
                    results[biz[j]['bizId']] = fscore + bscore

            
            if int(len(results)) >= 1:
                kh = sorted(results, key = results.__getitem__, reverse = True)
                print(feedshop)
                print(bdic[kh[0]])
                print('The biz is - ' + str(kh[0]) + ' total score is - ' + str(results[kh[0]]))
                d['feedId'] = feeds[i]['feedId']
                d['bizId'] = kh[0]
                d['userCatLevel1'] = feeds[i]['userCatLevel1']                          
                d['userCatLevel2'] = feeds[i]['userCatLevel2']              
                d['title'] = feeds[i]['title']
                d['textContent'] = feeds[i]['textContent']
                d['sourceDevice'] = feeds[i]['sourceDevice']
                
                fdup = requests.post(urlupdate, data = json.dumps(d), headers = {'Content-type': 'application/json'})
                if fdup.status_code == 200:
                    print('Successfully updated - ' + str(feeds[i]['feedId']))
                    t=1
                else:
                    print(' Update unsuccessful - ' + str(feeds[i]['feedId']))
                    notupdatedfeeds.append(feeds[i])                    
        else:
            notupdatedfeeds.append(feeds[i])
            
        if t == 0:
            notupdatedfeeds.append(feeds[i])
                
            

    if int(len(notupdatedfeeds)) >= 1:
        print('Feeds not updated are - \n')
        for i in range(len(notupdatedfeeds)):
            print(str(notupdatedfeeds[i]['feedId']))

    
                
    

    
