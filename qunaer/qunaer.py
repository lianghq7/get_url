# -*- coding:utf8 -*-  
# import urllib.request
import re
import time
import urllib
import urllib2
import requests 
import json
import random
from bs4 import BeautifulSoup
def main():
    # fp=open("lnyxy_qunaer300-399.txt","w")
    sightId= '300'
    
    beg_page = 120
    max_page = 199#max_page = 900

    fp=open("lnyxy_qunaer"+str(beg_page)+"-"+str(max_page)+".txt","w")
    headers ={'Host': 'piao.qunar.com',
'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate',
'X-Requested-With': 'XMLHttpRequest',
'Referer': 'http://piao.qunar.com/ticket/detail_3633837019.html?st=a3clM0QlRTUlQjIlQUQlRTUlOEQlOTclRTUlOEQlQjAlRTglQjElQTElRTUlOUIlQUQlMjZpZCUzRDMwMCUyNnR5cGUlM0QwJTI2aWR4JTNEMSUyNnF0JTNEbmFtZSUyNmFwayUzRDIlMjZzYyUzRFdXVyUyNmFidHJhY2UlM0Rid2QlNDAlRTYlOUMlQUMlRTUlOUMlQjAlMjZsciUzRCVFNSVCOSVCRiVFNSVCNyU5RSUyNmZ0JTNEJTdCJTdE',

'Cookie': 'JSESSIONID=94A930E070FE5F4B1E90B2DF0C8C0322; Request-Node=4adbd717b0cf64068dcecd220d9aef21; QN300=organic; QN1=O5cv5lnhzr0GAyeVgq6MAg==; csrfToken=94kqhWGl2gQkLAkrpRiCDbNlFLzF3Axq; QN67=300; QN58=1507970750396%7C1507970750396%7C1; QN57=15079707503970.19194137396801214; QN269=14A8DA80B0BC11E7A360FA163EF78B12; _i=RBTKA2fEAcHxc5sRseZ7Jncn9Yxx; _vi=yHmL0eO25HJSU2dKYVbwGRP8-a7OgEPEcFDixGh9qMy667elAOGDQNkivVDl9jpByMp1xZYqLC6pMT3v7MKbN0LDf4fp571PxleeIucTm67b1K-C4R3C2fV1h5WH4gfAk5WRYEykgSQYIr5Q63z9rAsn_69MxF9On2yLy0R27BQZ; Hm_lvt_15577700f8ecddb1a927813c81166ade=1507970752; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1507970752',
'Connection': 'keep-alive'}

    for page in range(beg_page, max_page + 1):
        print (str(page) + 'of' + str(max_page))
        url = 'http://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=' +sightId +'&index=' +str(page) +'&page=' + str(page) + '&pageSize=10&tagType=0'
        time.sleep(3+random.randint(1,4))
        source_code = requests.get(url, headers=headers)
        source_code.enconding = 'utf-8'
        
        temp_json_str = source_code.content
        # print (temp_json_str)
        json.loads(temp_json_str)

        json_all = json.loads(temp_json_str)

        for per_com in json_all['data']['commentList']:
            # print (per_com['content'])
            if (len(re.findall(r'用户未点评，系统默认好评。', per_com['content'].encode('utf8'))) == 0):
                print (per_com['content'].encode('utf8'))
                fp.write('{\'comment\':' + per_com['content'].encode('utf8') + ',\'score\':' + str(per_com['score']) + ',\'date\':' + per_com['date'].encode('utf8') + '}\n')
            # print (per_com['score'],per_com['date'])
        
    fp.close()

if __name__ == '__main__' :
    main()
