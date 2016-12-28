import requests
import json


urlfeeds = 'http://fyndox.herokuapp.com/api/selectFeeds'
urlupdate = 'http://fyndox.herokuapp.com/api/updateFeed'

fr = requests.get(urlfeeds)
feeds = fr.json()

def updatefeedscats():
  
    x = input('Enter starting feed id - ')
    y = input('Enter ending feed id - ')
    notupdated = []
    for i in range(len(feeds)):
        if int(feeds[i]['feedId']) >= int(x) and int(feeds[i]['feedId']) <= int(y):
            d={}
            d['feedId'] = feeds[i]['feedId']
            d['bizId'] = feeds[i]['bizId']
            d['title'] = feeds[i]['title']
            d['textContent'] = feeds[i]['textContent']
            d['sourceDevice'] = feeds[i]['sourceDevice']
            d['userCatLevel1'] = feeds[i]['sourceDevice']
            f = []
            
            #for j in range(len(feeds[i]['title'])):
#                f.append(feeds[i]['title'][j])
            #print(f)
            d['userCatLevel2'] = feeds[i]['userCategories']
            #print(d)

            fdup = requests.post(urlupdate, data = json.dumps(d), headers = {'Content-type': 'application/json'})
            if fdup.status_code == 200:
                print('Successfully updated - ' + str(feeds[i]['feedId']))
            else:
                print('Update unsuccessful - ' + str(feeds[i]['feedId']))
                notupdated.append(feeds[i]['feedId'])

            



    print('Not updated feeds - ' + str(len(notupdated)))
    for i in range(len(notupdated)):
        print(notupdated[i])
                

        
            
