# -*- coding:utf8 -*-  
# import urllib.request
import re
import urllib
import urllib2
import requests
from bs4 import BeautifulSoup
def main():
    fp=open("get_poi_id.txt","w")
    url = 'http://www.mafengwo.cn/ajax/router.php'
    max_page = 34
    for page in range(1, max_page + 1):
        d = {'sAct': 'KMdd_StructWebAjax|GetPoisByTag', 'iMddid': '10088', 'iTagId': '0', 'iPage':str(page)}
        res = requests.post(url, data=d)
        res_str = res.text.decode('unicode-escape').encode("utf8")
        print(res_str)
        poi_id_list = re.findall(r'<a href=".*?.html" target', res_str)
        poi_name_list = re.findall(r'target="_blank" title=".*?">', res_str)
        if len(poi_id_list) != len(poi_name_list):
            print ('error:len(poi_id_list) != len(poi_name_list)')
            break
        for (poi_name,poi_id) in zip(poi_name_list,poi_id_list):
            poi_name = poi_name.replace('target="_blank" title="', '').replace('">', '')
            print (poi_name)
            poi_id = poi_id.replace('<a href="\/poi\/', '').replace('.html" target', '')
            print (poi_id)
            fp.write(poi_name + ' ' + poi_id + '\n')  # '$'为停止符

    fp.close()

if __name__ == '__main__' :
    main()
