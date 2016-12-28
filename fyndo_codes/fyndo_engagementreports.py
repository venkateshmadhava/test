import json
import requests
import datetime
import time

urlusers = 'http://fyndox.herokuapp.com/api/selectUsers'
urlvwfeeds = 'http://fyndox.herokuapp.com/api/selectViewedFeeds'
urlfeeds = 'http://fyndox.herokuapp.com/api/selectFeeds'
urlopfeeds = 'http://fyndox.herokuapp.com/api/selectOpenedFeeds'
urlupvtfeeds = 'http://fyndox.herokuapp.com/api/selectUpvotedFeeds'

urq = requests.get(urlusers)
allusers = urq.json()

vwfrq = requests.get(urlvwfeeds)
allviewedfeeds = vwfrq.json()

frq = requests.get(urlfeeds)
feeds = frq.json()

opfrq = requests.get(urlopfeeds)
allopenedfeeds = opfrq.json()

upvtfrq = requests.get(urlupvtfeeds)
allupvotedfeeds = upvtfrq.json()

cats = []
feedscat = {}
bizvwdls = []
fdbzvw = {}

for i in range(len(feeds)):
    feedscat[feeds[i]['feedId']] = feeds[i]['sourceDevice']
    cats.append(feeds[i]['sourceDevice'])
    if feeds[i]['noOfBizClicks'] >= 1:
        gg = []
        gg.append(feeds[i]['bizId'])
        gg.append(feeds[i]['noOfBizClicks'])
        fdbzvw[feeds[i]['feedId']] = gg

cats = list(set(cats))
vwfeedscat = {}

for i in range(len(cats)):
    vwfeedscat[cats[i]] = 0



def newusers():
    venoid = '5843b3c0e4b075de98cc9119'
    t = 0
    f = 0
    users = []
    for i in range(len(allusers)):
        t = t+1
        if allusers[i]['userId'] == venoid:
            f = 1
        if f == 1:
            users.append(allusers[i])
    users.pop(0)
    h = 0

    for i in range(len(users)):
        if users[i]['fbProfile'] is None:
            j=0
        else:
            h=h+1
            
    print('All users - ' + str(t))
    print('The total number of users after 4 Dec - ' + str(len(users)))
    print('Fyndo users - ' + str(h))
    print('Biz users - ' + str(len(users)-h))

def newusersbydate():
    x = input('Enter start date - ')
    y = input('Enter end date - ')
    m = input('Enter month - ')
    users = []
    fl = 0
    for i in range(len(allusers)):
        try:
            timestamp = int(allusers[i]['dateOfBirth'])/1000000
            acttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))[0:10].split('-')
            fl = 1
        except:
            fl = 0

        if fl == 1:
            #print('fl is 1 for user - ' + str(allusers[i]['userId']) + ' and the date is - ' + ' :: '.join(acttime))
            if str(acttime[1]) == str(m):
                if int(acttime[2]) >= int(x) and int(acttime[2]) <= int(y):
                    users.append(allusers[i])

    print('The users who registered between ' + str(x) + ' and ' + str(y) + ' is - ' + str(len(users)))


def viewfeeds():
    capid = 1339
    vwfeeds = []
    acvwfeeds = []

    for keys in vwfeedscat:
        vwfeedscat[keys] = 0
    
    for i in range(len(allviewedfeeds)):
        if allviewedfeeds[i]['index'] >= 1339:
            timestamp = int(allviewedfeeds[i]['viewedDate'])/1000
            acttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))[0:10].split('-')
            allviewedfeeds[i]['date'] = acttime
            vwfeeds.append(allviewedfeeds[i])

    x = input('Enter start date - ')
    y = input('Enter end date - ')
    m = input('Enter month - ')
    t = 0
    usrvw = {}
    usrid = []
    latlong = []

    
    for i in range(len(vwfeeds)):
        if str(vwfeeds[i]['date'][1]) == str(m):
            if str(vwfeeds[i]['date'][2]) >= str(x) and str(vwfeeds[i]['date'][2]) <= str(y):
                if str(vwfeeds[i]['userId']) == "" or str(vwfeeds[i]['userId']) =='2-5843b3c0e4b075de98cc9119' or str(vwfeeds[i]['userId']) == '2-5841b68ae4b0e344a564b14b' or str(vwfeeds[i]['userId']) == '2-583fbdcce4b0683c635bcc85' or str(vwfeeds[i]['userId']) == '2-583edf13e4b0e1f75b9532c1':
                    #do nothing
                    xxxx=0
                else:
                    t = t+1
                    acvwfeeds.append(vwfeeds[i])
                    usrid.append(vwfeeds[i]['userId'])
                    ltlg = []
                    ltlg.append(vwfeeds[i]['gpsLatitude'])
                    ltlg.append(vwfeeds[i]['gpsLongitude'])
                    latlong.append(ltlg)

    usrid = list(set(usrid))
    for i in range(len(usrid)):
        usrvw[usrid[i]] = []

    for i in range(len(acvwfeeds)):
        for j in range(len(acvwfeeds[i]['viewedFeedIds'])):
                       usrvw[acvwfeeds[i]['userId']].append(acvwfeeds[i]['viewedFeedIds'][j])
            
    print('The total sessions between - ' + str(x) + ' and ' + str(y) + ' is - ' + str(t)) 
    print('The total #users viewed feeds is - ' + str(len(usrvw)))

    totalbizviewed = 0
    totalfeedsviewed = 0
    for keys in usrvw:
        print('User is - ' + str(keys) + ' - Total - ' + str(len(usrvw[keys])))
        totalfeedsviewed = totalfeedsviewed + len(usrvw[keys])
        for r in range(len(usrvw[keys])):
            try:
                vwfeedscat[feedscat[usrvw[keys][r]]] = vwfeedscat[feedscat[usrvw[keys][r]]]+1
            except:
                ffff = 0
            try:
                fdbzvw[usrvw[keys][r]]
                totalbizviewed = totalbizviewed + 1
            except:
                xxxxxx = 0
        

    print('The total number of feeds viewed is - ' + str(totalfeedsviewed))
    print('The total number of biz viewed is - ' + str(totalbizviewed))
    print('The avg feeds viewed per user is - ' + str(totalfeedsviewed/len(usrvw)))
    
    #include code to group viewed feeds by category.
    print('The category wise numbers are - ')
    for keys in vwfeedscat:
        print(str(keys) + ' - ' + str(vwfeedscat[keys]))
    #include code to check % of posts too.

    print('The lat longs of users who viewedfeeds are - ')
    for k in range(len(latlong)):
        sk = str(latlong[k][0]) + "," + str(latlong[k][1])
        print(sk)
    

def openfeeds():
    cap = 1082
    opfeeds = []
    acopfeeds = []
    for i in range(len(allopenedfeeds)):
        if allopenedfeeds[i]['index'] >= cap:
            timestamp = int(allopenedfeeds[i]['openedDate'])/1000
            acttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))[0:10].split('-')
            allopenedfeeds[i]['date'] = acttime
            opfeeds.append(allopenedfeeds[i])

    x = input('Enter start date - ')
    y = input('Enter end date - ')
    m = input('Enter month - ')
    t = 0
    usrid = []
    usrop = {}
    latlong = []

    for i in range(len(opfeeds)):
        if str(opfeeds[i]['date'][1]) == str(m):
            if str(opfeeds[i]['date'][2]) >= str(x) and str(opfeeds[i]['date'][2]) <= str(y):
                if str(opfeeds[i]['userId']) == "2-" or str(opfeeds[i]['userId']) =='2-5843b3c0e4b075de98cc9119' or str(opfeeds[i]['userId']) == '2-5841b68ae4b0e344a564b14b' or str(opfeeds[i]['userId']) == '2-583fbdcce4b0683c635bcc85' or str(opfeeds[i]['userId']) == '2-583edf13e4b0e1f75b9532c1':
                    #do nothing
                    xxxx = 0
                else:
                    t = t+1
                    acopfeeds.append(opfeeds[i])
                    usrid.append(opfeeds[i]['userId'])
                    ltlg = []
                    ltlg.append(opfeeds[i]['gpsLatitude'])
                    ltlg.append(opfeeds[i]['gpsLongitude'])
                    latlong.append(ltlg)
                    

    usrid = list(set(usrid))
    for i in range(len(usrid)):
        usrop[usrid[i]] = []
        
    for i in range(len(acopfeeds)):
        usrop[acopfeeds[i]['userId']].append(acopfeeds[i]['openedFeedId'])
        
    print('The total feeds opened between - ' + str(x) + ' and ' + str(y) + ' is - ' + str(t))
    print('The total #users opened feeds is - ' + str(len(usrop)))

    for keys in usrop:
        print('User is - ' + str(keys) + ' - Total opened is - ' + str(len(usrop[keys])))

    print('The avg feeds opened per user is - ' + str(t/len(usrop)))

    print('The lat longs of users who opened feeds are - ')
    for k in range(len(latlong)):
        sk = str(latlong[k][0]) + "," + str(latlong[k][1])
        print(sk)

def upvotedfeeds():
    upfeeds = []
    acupfeeds = []
    cap = 0
    for i in range(len(allupvotedfeeds)):
        if allupvotedfeeds[i]['index'] >= cap:
            timestamp = int(allupvotedfeeds[i]['upvotedDate'])/1000
            acttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))[0:10].split('-')
            allupvotedfeeds[i]['date'] = acttime
            upfeeds.append(allupvotedfeeds[i])
            
    x = input('Enter start date - ')
    y = input('Enter end date - ')
    m = input('Enter month - ')
    t = 0
    usrid = []
    usrup = {}
    
    for i in range(len(upfeeds)):
        if str(upfeeds[i]['date'][1]) == str(m):
            if str(upfeeds[i]['date'][2]) >= str(x) and str(upfeeds[i]['date'][2]) <= str(y):
                if str(upfeeds[i]['userId']) == "" or str(upfeeds[i]['userId']) =='5843b3c0e4b075de98cc9119' or str(upfeeds[i]['userId']) == '5841b68ae4b0e344a564b14b' or str(upfeeds[i]['userId']) == '583fbdcce4b0683c635bcc85' or str(upfeeds[i]['userId']) == '583edf13e4b0e1f75b9532c1':
                    #do nothing
                    xxxx = 0
                else:
                    t = t+1
                    acupfeeds.append(upfeeds[i])
                    usrid.append(upfeeds[i]['userId'])

    usrid = list(set(usrid))
    for i in range(len(usrid)):
        usrup[usrid[i]] = []

    for i in range(len(acupfeeds)):
        usrup[acupfeeds[i]['userId']].append(acupfeeds[i]['upvotedFeedId'])

    print('The total feeds upvoted between - ' + str(x) + ' and ' + str(y) + ' is - ' + str(t))
    print('The total #users upvoted feeds is - ' + str(len(usrup)))

    for keys in usrup:
        print('User is - ' + str(keys) + ' - Total opened is - ' + str(len(usrup[keys])))

    print('The avg feeds upvoted per user is - ' + str(t/len(usrup)))
    
    

    

    
            

    
