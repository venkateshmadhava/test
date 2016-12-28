import json
import copy
import sys
sys.path.append('/Library/Python/2.7/site-packages')
import requests
import geopy
from geopy.distance import vincenty


#initializing other variables
urlput = 'http://fyndo.herokuapp.com/api/insertBizInfo'

frq = requests.get('http://fyndox.herokuapp.com/api/selectFeeds')
feeds = frq.json()

bizrq = requests.get('http://fyndox.herokuapp.com/api/selectBizInfos')
biz = bizrq.json()

b={}

def feedstobiz():
    t = 0
    ins = 0
    stfdid = input('Enter starting feed id to convert to biz - ')
    enfdid = input('Enter ending feed id to convert to biz - ')
    bizdic = {}
    biztoinsert = []
    biznotinserted = []
    bizin = {}

    for i in range(len(biz)):
        bizdic[biz[i]['bizId']] = {}
        bizdic[biz[i]['bizId']]['bizId'] = biz[i]['bizId']
        bizdic[biz[i]['bizId']]['lat'] = biz[i]['gpsLatitude']
        bizdic[biz[i]['bizId']]['long'] = biz[i]['gpsLongitude']
        try:
            bizdic[biz[i]['bizId']]['name'] = biz[i]['bizName'].lower().split(" ")
        except:
            bizdic[biz[i]['bizId']]['name'] = ""

    bizv = list(bizdic.values())

    
    for x in range(len(bizv)):
                try:
                    bizv[x]['name'].remove('')
                    bizv[x]['name'].remove(' ')
                    bizv[x]['name'].remove('store')
                    
                except:
                    mmm = 0

    print(bizv[300])
    
    for i in range(len(feeds)):
        if int(feeds[i]['feedId']) >= int(stfdid) and int(feeds[i]['feedId']) <= int(enfdid):
            ins = ins + 1
            match = 0
            fdltlg = (feeds[i]['gpsLatitude'],feeds[i]['gpsLongitude'])
            
            
            try:
                fshop = feeds[i]['shopName'].lower().split(" ")
                fshop.remove(' ')
                fshop.remove('')
                fshop.remove('store')
            except:
                mm = 0

            for p in range(len(bizv)):
                fscore = 0.0000
                bscore = 0.0000
                dis = 0
                bzltlg = (bizv[p]['lat'],bizv[p]['long'])
                for h in range(len(fshop)):
                    if fshop[h] in bizv[p]['name']:
                        fscore = fscore + 1
                        
                for j in range(len(bizv[p]['name'])):
                    if bizv[p]['name'][j] in fshop:
                        bscore = bscore + 1
                        
                if int(vincenty(fdltlg,bzltlg).meters) <= 25:
                    dis = 1
                else:
                    dis = 0
                
                try:
                    fscore = fscore/len(fshop)
                    bscore = bscore/len(bizv[p]['name'])
                except:
                    mnhn = 0
                    
                if fscore > 0.5 or bscore > 0.5 and dis == 1:
                    match = 1
                    existingbizid = (str(bizv[p]['bizId']) + ' - ' + ' '.join(bizv[p]['name']))
                    
                else:
                    hghgfgjjg = 0
    
                      
            if match == 0:
                biztoinsert.append(feeds[i]['shopName'])
                bizin[feeds[i]['shopName']] = {}
                bizin[feeds[i]['shopName']]['bizName'] = feeds[i]['shopName']
                bizin[feeds[i]['shopName']]['bizDesc'] = feeds[i]['title']
                bizin[feeds[i]['shopName']]['bizCategory'] = feeds[i]['sourceDevice']
                bizin[feeds[i]['shopName']]['bizStreetAddress'] = feeds[i]['shopArea']
                bizin[feeds[i]['shopName']]['lat'] = feeds[i]['gpsLatitude']
                bizin[feeds[i]['shopName']]['long'] = feeds[i]['gpsLongitude']
                bizin[feeds[i]['shopName']]['area'] = feeds[i]['shopArea']
                bizin[feeds[i]['shopName']]['feedid'] = feeds[i]['feedId']
            else:
                hhh = ('Already exists - ' + str(feeds[i]['feedId']) + ' - ' + feeds[i]['shopName'] + ' ---bizinfo--- ' + existingbizid)
                biznotinserted.append(hhh)
                

    biztoinsert = list(set(biztoinsert))


    for i in range(len(biztoinsert)):
        #insert biz here            
        d = {}
        d['bizName'] = bizin[biztoinsert[i]]['bizName']
        d['bizDesc'] = bizin[biztoinsert[i]]['bizDesc']
        d['bizType'] = 'Store'           
        d['bizMobile'] = ''
        d['bizCategory'] = bizin[biztoinsert[i]]['bizCategory']
        d['userRelation'] = ''
        d['bizStreetAddress'] = bizin[biztoinsert[i]]['bizStreetAddress']
        d['bizProfile'] = ''
        d['gpsLatitude'] = bizin[biztoinsert[i]]['lat']
        d['gpsLongitude'] = bizin[biztoinsert[i]]['long']
        d['fyndoUserId']= '9999'
        d['bizClaimDate'] = ''
        areaf = str(bizin[biztoinsert[i]]['bizStreetAddress'])           
        arlt = areaf.split(', ')
        #print(arlt)
        if int(len(arlt))>2 and 'Chennai' in arlt:
            for j in range(len(arlt)):
                if str(arlt[j].lower()) == 'Chennai'.lower():
                    x=j
            d['bizArea']=str(arlt[x-1])
        else:
            d['bizArea']=''
        #print(json.dumps(d))                   
        r = requests.post(urlput, data = json.dumps(d), headers = {'Content-type': 'application/json'})
        if int(r.status_code) == 200:
            print('Biz successfull inserted for - ' + str(bizin[biztoinsert[i]]['bizName']) + ' (' + str(bizin[biztoinsert[i]]['feedid']) + ')')
            t = t+1
        else:
            ts = bizin[biztoinsert[i]]['feedid'] + ' - ' + bizin[biztoinsert[i]]['bizName']
            biznotinserted.append(ts)


    
    print('\n\n')
    print('The total number of feeds processed is - ' + str(ins))
    print('The total number of biz inserted is - ' + str(t))
    
    print('The biz not inserted - ')
    for l in range(len(biznotinserted)):
        print(biznotinserted[l])
        
                
            











