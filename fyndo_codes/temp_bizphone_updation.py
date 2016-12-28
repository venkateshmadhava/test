import xlrd
import json
import requests

urlup = 'http://fyndox.herokuapp.com/api/updateBizInfo'
urlbiz = 'http://fyndox.herokuapp.com/api/selectBizInfos'
br = requests.get(urlbiz)
biz = br.json()
bizdic = {}

for i in range(len(biz)):
    bizdic[biz[i]['bizId']] = biz[i]

d = {
    "bizId": 1107,
    "bizName": "Starbucks Pvt Ltd",
    "bizDesc": "Coffee",
    "bizType": "Eatery",
    "bizArea": "Chennai",
    "bizCategory": "Coffee",
    "userRelation" : "Manager",
    "bizProfile" : "",
    "gpsLatitude": 13.0219857,
    "gpsLongitude": 80.0573971,
    "fyndoUserId" : "57f56975e4b0c4c7a6cecedb",
    "bizClaimDate": "1477758241"
  }

for keys in d:
    d[keys] = ""


wkbook = xlrd.open_workbook('/Users/venkateshmadhava/Desktop/phone.xlsx')
sheet = wkbook.sheet_by_index(0)
rows = 5
bizphones = {}
for i in range(rows):
    bizphones[int(sheet.cell(i, 0).value)] = int(sheet.cell(i,1).value)

print('the len of bizphones - ' + str(len(bizphones)))
print(bizphones)


x = input('Enter starting biz id - ')
y = input('Enter ending biz id - ')

for keys1 in bizphones:
    if int(keys1) >= int(x) and int(keys1) <= int(y):
        for keys2 in d:
            d[keys2] = bizdic[keys1][keys2]
        
        try:
            d['bizClaimDate'] = int(d['bizClaimDate'])/1000
        except:
            d['bizClaimDate'] = ""
            
        d['bizLandline'] = bizphones[keys1]
        print(d)
        #update code
        bdup = requests.post(urlup, data = json.dumps(d), headers = {'Content-type': 'application/json'})
        if bdup.status_code == 200:
            print('Success update - ' + str(keys1))
        else:
            print('Not updated - ' + str(keys1))
            
    
    
