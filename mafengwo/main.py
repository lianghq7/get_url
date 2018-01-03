# -*- coding:utf8 -*-  
import re
import urllib
import urllib2
from bs4 import BeautifulSoup

path = '/data/'
def main():
    line_count = 119
    for line in open("get_poi_id.txt","r").readlines():
    	line_count += 1
        each_item = line.split()
        read_name = each_item[0]
        read_id = each_item[1]
        txt_name = read_name + '.txt'
        fp=open(txt_name,"w")
        url_first = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?&params={"poi_id":"' + str(read_id) + '","page":1,"just_comment":1}'
        req = urllib2.Request(url_first)
        res_data = urllib2.urlopen(req)
        res = res_data.read().decode('unicode-escape').encode("utf8")
        soup = BeautifulSoup(res, "lxml", from_encoding="utf-8")
        if len(soup.find_all(class_='count')) == 0:
        	page_num = '1'
        else:
            rev = soup.find_all(class_='count')[0]
            rev_text = rev.get_text().encode("utf8").strip()
            page_num = re.findall(r'共.*?页', rev_text)[0].replace('共','').replace('页','')

        max_page = int(page_num)
        for page in range(1, max_page + 1):
            print(page, 'of', max_page, 'in', line_count)

            url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?'+'&params={"poi_id":"' + str(read_id) + '","page":' + str(page) + ',"just_comment":1}'
            # url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery'+ jQuery + '&params={"poi_id":"' + poi_id + '","page":' + str(page) + ',"just_comment":1}'
            req = urllib2.Request(url)

            res_data = urllib2.urlopen(req)
            res = res_data.read().decode('unicode-escape').encode("utf8")
            soup = BeautifulSoup(res, "lxml", from_encoding="utf-8")
            rev_txt_list = soup.find_all(class_='rev-txt')
            for rev in rev_txt_list:
                rev_text = rev.get_text().encode("utf8").strip()
                fp.write('$' + rev_text + '$\n')  # '$'为停止符
                # print (rev_text)
    
        fp.close()

if __name__ == '__main__' :
    main()
