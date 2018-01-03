# -*- coding:utf8 -*-  
# import urllib.request
import re
import urllib
import urllib2
import requests
from bs4 import BeautifulSoup
def main():
    fp=open("lnyxy_xiecheng.txt","w")
    url = 'http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView'
    max_page = 115 #116
    for page in range(1, max_page + 1):
        print (str(page) + 'of' + str(max_page))
        d = {'poiID': '91849', 'districtId': '152', 'districtEName': 'Guangzhou', 'pagenow':str(page), 
        'order': '3.0', 'star': '0.0', 'tourist': '0.0', 'resourceId':'110338', 'resourcetype':'2'}
        res = requests.post(url, data=d)
        res_str = res.text.encode("utf8")
        soup_string = BeautifulSoup(res_str, "html.parser")
        # print (soup_string)
        # print ('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        all_div = soup_string.find(attrs={"class":"comment_ctrip"})
        per_div = all_div.findAll(attrs={"class":"comment_single"})
        for div in per_div:
            str_all_score = ''
            str_scene = ''
            str_interest = ''
            str_price = ''
            top_content = div.find(attrs={"class":"title cf"})
            # print(type(top_content))
            str_top_content = str(top_content)
            # print(type(str_top_content))
            comment = div.find(attrs={"class":"heightbox"})
            str_comment = str(comment)
            str_comment = str_comment.replace('<span class="heightbox">', '').replace('</span>', '')
            fp.write('{\'comment\':' + str_comment + ',')
            all_score = re.findall(r'<span style="width:.*?%;">', str_top_content) #<span style="width:60%;">
             
            if (len(all_score) > 0):
                str_all_score = all_score[0].replace('<span style="width:','').replace('%;">','')
                fp.write('\'score\':' + str_all_score)
            scene = re.findall(r'景色：\d', str_top_content)

            if (len(scene) > 0):
                str_scene = scene[0].replace('景色：','')
                fp.write(',\'scene\':' + str_scene)
            interest = re.findall(r'趣味：\d', str_top_content)

            if (len(interest) > 0):
                str_interest = interest[0].replace('趣味：','')
                fp.write(',\'interest\':' + str_interest)
            price = re.findall(r'性价比：\d', str_top_content)
 
            if (len(price) > 0):
                str_price = price[0].replace('性价比：','')
                fp.write(',\'price\':' + str_price)
            # data_or_way = re.findall(r'<span class="youcate.*?</span>', top_content)
            data_or_way = div.find(attrs={"class":"youcate"})
            str_data_or_way = str(data_or_way)
            temp_data = re.findall(r'\d\d\d\d-.*?出游', str_data_or_way)
            if (len(temp_data) > 0):
                data = temp_data[0].replace(' 出游', '')
                fp.write(',\'data\':' + data)
            temp_way = re.findall(r'class="youcate_.*?></i>', str_data_or_way)
            if (len(temp_way) > 0):
                way = re.findall(r'title=".*?"', temp_way[0])[0].replace('title="', '').replace('"', '')
                fp.write(',\'way\':' + way)

            fp.write('}\n')

            # text_class_score = div.find(attrs={"class":"youcate"}) #景色：5趣味：5性价比：5
            # print(comment)
            # print(str_all_score)
            
            # print(str_scene)
            # print(str_price)
            # print(data_or_way)
        
    fp.close()

if __name__ == '__main__' :
    main()
