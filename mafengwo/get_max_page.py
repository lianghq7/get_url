import re
from urllib import request

def main():
    line_count = 1
    for line in open("get_poi_id.txt","r").readlines():
        if line_count < 1:
            break
        line_count -= 1
        each_item = line.split()
        read_name = each_item[0]
        read_id = each_item[1]
        url_main = 'http://www.mafengwo.cn/poi/' + read_id + '.html'
        print (url_main)
        response = request.urlopen(url_main)
        page = response.read()
        page = page.decode('utf-8')
        print (page)
        page_text = re.findall(r'共.*?页', page)
        print (page_text)

if __name__ == '__main__' :
    main()
