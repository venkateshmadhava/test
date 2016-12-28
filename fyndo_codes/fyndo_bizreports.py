import json
import requests
import datetime
import time

url = 'http://fyndox.herokuapp.com/api/selectBizInfos'
resp = requests.get(url)
biz = resp.json()

urlfeed = 'http://fyndox.herokuapp.com/api/selectFeeds'
fr = requests.get(urlfeed)
feeds = fr.json()

urluser = 'http://fyndox.herokuapp.com/api/selectUsers'
urq = requests.get(urluser)
users = urq.json()



def bizsignedup():
    t = 0
    for i in range(len(biz)):
        if str(biz[i]['fyndoUserId']) != '9999':
            t = t+1
            timestamp = biz[i]['bizCreatedDate']/1000
            acttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            print(str(acttime) + ' - ' + str(biz[i]['bizName']))
    print('The total number of biz signedup is - ' + str(t))


def bizengage():
    f = 0
    bizusers = []
    bizfeeds = []
    t = 0
    
    for i in range(len(users)):
        if users[i]['fbProfile'] is None:
            if users[i]['userId'] == '57fc99b2e4b08a37fc1f2ff5':
                f = 1
            if f == 1:
                bizusers.append(users[i]['userId'])
    
    for i in range(len(feeds)):
        if feeds[i]['userId'] in bizusers:
            tme = feeds[i]['dateOfPost']/1000
            act = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tme))[0:10].split('-')
            feeds[i]['date'] = act
            bizfeeds.append(feeds[i])

    print('Total biz users - ' + str(len(bizusers)))
    print('Total feeds posted by biz - ' + str(len(bizfeeds)))
    for i in range(len(bizfeeds)):
        print(bizfeeds[i]['feedId'])

    x = input('Enter starting date - ')
    y = input('Enter ending date - ')
    m = input('Enter month - ')

    for i in range(len(bizfeeds)):
        if bizfeeds[i]['date'][1] == m:
            if bizfeeds[i]['date'][2] >= x and bizfeeds[i]['date'][2] <= y:
                t = t+1
   
    print('The feeds posted by biz in the given date range is - ' + str(t))
            
        
    


                                                    
