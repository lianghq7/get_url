# -*- coding:utf8 -*-  
# import urllib.request
import re
import time
import urllib
import csv

# import urllib2
from sys import argv
import requests
import json
import random
from bs4 import BeautifulSoup
import get_server_id

file_path = 'csv/'
txt_path = 'txt/'
def main():
    print ('请选择类型')
    print ('4.枪矛 52.宝珠 18.铠甲 59.女衣 17.头盔 58.发钗 19.鞋子 20.腰带 21.饰物')

    
    server_to_area = {'39': '33', '3': '3', '407': '29', '199': '49'}
    server_to_name = {'39': '世界之窗', '3': '国子监', '407': '曲阜孔庙', '199': '汴梁城'}
    kindid_to_name = {'4': '枪矛', '52':'宝珠', '18':'铠甲', '19':'鞋子', '59':'女衣', '17':'头盔', '58':'发钗', '20':'腰带', '21':'饰物'}
    # server_id = argv[1]
    # areaid = server_to_area[server_id]
    # server_name = server_to_name[server_id]
    kindid = input('请输入类型编号:')

    
    level_to_wuqi_shanghai = {'60': 128, '70': 148, '80': 168, '90': 280, '100': 310, '110': 340, '120': 370, '130': 400, '140': 430, '150': 460, '160': 490}
    level_to_wuqi_mingzhong ={'60': 160, '70': 184, '80': 208, '90': 325, '100': 360, '110': 395, '120': 430, '130': 465, '140': 500, '150': 535, '160': 571}
    level_to_toukui_fangyu = {'60': 26, '70': 30, '80': 34, '90': 50, '100': 55, '110': 60, '120': 65, '130': 70, '140': 75, '150': 80, '160': 84}
    level_to_yifu_fangyu = {'60': 80, '70': 88, '80': 100, '90': 145, '100': 160, '110': 175, '120': 190, '130': 205, '140': 220, '150': 235, '160': 249}
    level_to_yaodai_fangyu = {'60': 26, '70': 30, '80': 34, '90': 50, '100': 55, '110': 60, '120': 65, '130': 70, '140': 75, '150': 80, '160': 84}
    level_to_yaodai_qixue = {'60': 120, '70': 140, '80': 160, '90': 190, '100': 210, '110': 230, '120': 250, '130': 270, '140': 290, '150': 310, '160': 329}
    level_to_xianglian_lingli = {'60': 56, '70': 65, '80': 77, '90': 113, '100': 125, '110': 137, '120': 149, '130': 161, '140': 173, '150': 185, '160': 196}
    level_to_xiezi_fangyu = {'60': 24, '70': 27, '80': 29, '90': 50, '100': 55, '110': 60, '120': 65, '130': 70, '140': 75, '150': 80, '160': 84}
    level_to_xiezi_minjie = {'60': 23, '70': 26, '80': 29, '90': 32, '100': 35, '110': 38, '120': 41, '130': 44, '140': 47, '150': 50, '160': 52}
    
    dict_value_to_name = {1: '红玛瑙', 2: '太阳石', 3: '舍利子', 4: '光芒石', 5: '月亮石', 6: '黑宝石', 7: '神秘石', 8: '红宝石', 9: '黄宝石', 10: '蓝宝石', 11: '绿宝石', 12: '翡翠石'}
    


    #设置要爬取的大区和服务器，第一个参数是大区，第二个参数是服务器，某个参数若设为‘-1’，则表示全部，缺省值为‘-1’
    area_server_list = get_server_id.get_area_server()
    server_count = 0
    server_sum = len(area_server_list)
    for each_area_server in area_server_list:
        server_count += 1
        areaid = each_area_server[0]
        server_id = each_area_server[1]
        server_name = each_area_server[2]
        print (areaid, server_id, server_name)

    
        url1 = 'http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?&act=recommd_by_role&server_id=' + server_id + '&areaid=' + areaid + '&server_name=' + server_name + '&page=1&kindid=' + kindid + '&special_mode=and&hide_lingshi=1&count=15'
        source_code = requests.get(url1)
        temp_json_str = source_code.content
        final = temp_json_str.decode('unicode_escape')
        
        local_begin = final.find('"other_info":')
        data = ''
        while (local_begin > 0):
            local_end = final.find('"expire_time":', 10)
            data += final[:local_begin]
            final = final[local_end:]
            local_begin = final.find('"other_info":')
        data += final
        # print (data)
        
        dict_data = json.loads(data)
        total_pages = dict_data["pager"]["total_pages"]
        # total_pages = 2#for testing, reduce the time
        # total_pages = int(re.findall(r'"total_pages": \d+', final)[0].replace('"total_pages": ', '').replace(' ', ''))
        # print('total_pages:',total_pages)


        fp=open(txt_path + server_name + "-" + kindid_to_name[kindid] + "-" + str(total_pages) + "页.txt","w")
        csvout = open(file_path + server_name + "-" + kindid_to_name[kindid] + "-" + str(total_pages) + "页.csv", "w", newline='')
        firt_row = ['price_int', 'kindid','equip_level','server_id','equip_name','hole_num', '失败次数',
        '锻炼等级', '镶嵌宝石', '红玛瑙', '太阳石', '舍利子', '光芒石', '月亮石', '黑宝石', '神秘石', '翡翠石', '红宝石',
        '初伤（包含命中）', '初伤（不含命中）', '初防', '初血', '初敏', '初灵', '总伤',
        '红玛瑙加成', '太阳石加成', '舍利子加成', '光芒石加成', '月亮石加成', '翡翠石加成', '红宝石加成',
        '红玛瑙段数', '太阳石段数', '舍利子段数', '光芒石段数', '月亮石段数', '黑宝石段数', '神秘石段数', '翡翠石段数', '红宝石段数',
        '伤害', '爆伤害', '命中', '爆命中', '防御', '爆防御', '气血', '爆气血', '灵力', '爆灵力', '躲避', '敏捷', '爆敏捷', '敏捷点', '速度', '体质', '耐力',
        '魔力', '力量', '特技', '罗汉金钟', '晶清诀', '笑里藏刀', '破血狂攻', '破碎无双', '慈航普度', '四海升平', '玉清诀',
        '放下屠刀', '野兽之力', '流云诀', '凝滞术', '光辉之甲', '破甲术', '水清诀', '弱点击破', '聚精会神', '燃烧之光',
        '起死回生', '回魂咒', '圣灵之甲', '碎甲术', '河东狮吼', '魔兽之印', '啸风诀', '停陷术', '先发制人', '菩提心佑',
        '吸血', '残月', '命归术', '虚空之刃', '气疗术', '心疗术', '命疗术', '凝气诀', '凝神决', '气归术', '冰清诀',
        '诅咒之伤', '诅咒之亡', '绝幻魔音', '太极护法', '修罗咒', '天衣无缝', '冥王暴杀', '乾坤斩', '帝释无双', '伽罗无双',
        '亡灵之刃', '死亡之音', '身似菩提', '心如明镜', '移形换影', '凝心决', '毁灭之光', '金刚不坏', '特效', '无级别', '愤怒',
        '永不磨损', '简易', '暴怒', '神农', '神佑', '精致', '绝杀', '专注', '必中', '160级装备特性', '星位', '套装效果', '人造']
        writer = csv.DictWriter(csvout, fieldnames=firt_row)
        writer.writeheader()
        set_eid = set()    #用集合来通过“eid”去除重复出现的物品
        for page in range(1, total_pages + 1):
            print (str(page) + 'of' + str(total_pages))
            url2 = 'http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?&act=recommd_by_role&server_id=' + server_id + '&areaid=' + areaid + '&server_name=' + server_name + '&page=' + str(page) +'&kindid=' + kindid + '&hide_lingshi=1&count=15'
            url =  'http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?&act=recommd_by_role&server_id=173&areaid=39&server_name=逍遥城&page=2&kindid=20&hide_lingshi=1&count=15'
            time.sleep(1+random.randint(1,4))    #每次爬取一页之前，暂停3秒。
            source_code = requests.get(url2)
            # source_code.enconding = 'utf-8'
            
            temp_json_str = source_code.content
            # tempstr = unicode(temp_json_str,"gb2312")
            final = temp_json_str.decode('unicode_escape')

            local_begin = final.find('"other_info":')
            data = ''
            while (local_begin > 0):
                local_end = final.find('"expire_time":', 10)
                data += final[:local_begin]
                final = final[local_end:]
                local_begin = final.find('"other_info":')
            data += final
            # print (data)
        
            dict_data = json.loads(data)

            fp.write(data)
            # json.loads(temp_json_str)

            each_15 = dict_data['equips']

            for each in each_15:
                try:
                    eid = each['eid']
                    # print (eid)
                    if eid not in set_eid:
                        set_eid.add(eid)
                    else:
                        continue
                    hole_num = '0'
                    failtime = '0'
                    baoshi_level = '0'
                    baoshi = ''
                    xingwei = '0'
                    shanghai = '0'
                    mingzhong = '0'
                    fangyu = '0'
                    qixue = '0'
                    duobi = '0'
                    lingli = '0'
                    minjie = '0'

                    baoshanghai = '0'
                    baomingzhong = '0'
                    baofangyu = '0'
                    baoqixue = '0'
                    baolingli = '0'
                    baominjie = '0'
                    
                    taiyangshijiacheng = '0'
                    hongmanaijiacheng = '0'
                    yueliangshijiacheng = '0'
                    guangmangshijiacheng = '0'
                    shelizijiacheng = '0'
                    feicuishijiacheng = '0'
                    hongbaoshijiacheng = '0'

                    minjiedian = '0'
                    sudu = '0'
                    tizhi = '0'
                    naili = '0'
                    moli = '0'
                    liliang = '0'
                    teji = ''
                    texiao = ''
                    taozhuang = ''
                    zhuangbeitexing = ''
                    # '红玛瑙', '太阳石', '舍利子', '光芒石', '月亮石', '黑宝石', '神秘石', '翡翠石','红宝石'
                    hongmanai = '0'
                    taiyangshi = '0'
                    shelizi = '0'
                    guangmangshi = '0'
                    yueliangshi = '0'
                    heibaoshi = '0'
                    shenmishi = '0'
                    feicuishi = '0'
                    hongbaoshi = '0'
                    # '红玛瑙段数', '太阳石段数', '舍利子段数', '光芒石段数', '月亮石段数', '黑宝石段数', '神秘石段数', '翡翠石段数', '红宝石段数'
                    hongmanaiduanshu = '0'
                    taiyangshiduanshu = '0'
                    sheliziduanshu = '0'
                    guangmangshiduanshu = '0'
                    yueliangshiduanshu = '0'
                    heibaoshiduanshu = '0'
                    shenmishiduanshu = '0'
                    feicuishiduanshu = '0'
                    hongbaoshiduanshu = '0'

                    wujibie = '0'
                    bumo = '0'
                    fennu = '0'
                    jianyi = '0'
                    baonu = '0'
                    jingzhi = '0'
                    zhuanzhu = '0'
                    juesha = '0'
                    shennong = '0'
                    shenyou = '0'
                    bizhong = '0'


                    luohanjinzhong = '0'
                    jingqingjue = '0'
                    xiaolicangdao = '0'
                    poxuekuanggong = '0'
                    posuiwushaung = '0'
                    cihangpudu = '0'
                    sihaishengping = '0'
                    yuqingjue = '0'
                    fangxiatudao = '0'
                    yeshouzhili = '0'
                    liuyunjue = '0'
                    ningzhishu = '0'
                    guanghuizhijia = '0'
                    pojiashu = '0'
                    shuiqingjue = '0'
                    ruodianjipo = '0'
                    jujinghuishen = '0'
                    ranshaozhiguang = '0'
                    qisihuisheng = '0'
                    huihunzhou = '0'
                    shenglingzhijia = '0'
                    suijiashu = '0'
                    hedongshihou = '0'
                    moshouzhiyin = '0'
                    xiaofengjue = '0'
                    tingxianshu = '0'
                    xianfazhiren = '0'
                    putixinyou = '0'
                    xixue = '0'
                    canyue = '0'
                    mingguishu = '0'
                    xukongzhiren = '0'
                    qiliaoshu = '0'
                    xinliaoshu = '0'
                    mingliaoshu = '0'
                    ningqijue = '0'
                    ningshenjue = '0'
                    qiguishu = '0'
                    bingqingjue = '0'
                    zuzhouzhishang = '0'
                    zuzhouzhiwang = '0'
                    juehuanmoyin = '0'
                    taijihufa = '0'
                    xiuluozhou = '0'
                    tianyiwufeng = '0'
                    mingwangbaosha = '0'
                    qiankunzhan = '0'
                    dishiwushuang = '0'
                    jialuowushuang = '0'
                    wanglingzhiren = '0'
                    siwangzhiyin = '0'
                    shensiputi = '0'
                    xinrumingjing = '0'
                    yixinghuanying = '0'
                    ningxinjue = '0'
                    huimiezhiguang = '0'
                    jingangbuhuai = '0'

                    # print (each)
                    equip_level_desc = str(each['level'])

                    price_int = str(each['price_int'])

                    server_id = str(each['server_id'])
                    # print(server_id)
                    desc = each['desc']
                    
                    kindid = str(each['kindid'])
                    # print(kindid)
                    if (len(re.findall(r'制造者：', desc)) > 0):
                        renzao = '1'
                    else:
                        renzao = '0'
                    # print(renzao)
                    if (len(re.findall(r'修理失败 \d次', desc)) > 0):
                        failtime = re.findall(r'修理失败 \d次', desc)[0].replace('修理失败 ', '').replace('次', '')
                    # print(failtime)
                    equip_name = each['equip_name']
                    # print(equip_name)




                    if (len(re.findall(r'锻炼等级 \d+', desc)) > 0):
                        baoshi_level = re.findall(r'锻炼等级 \d+', desc)[0].replace('锻炼等级 ', '')
                        baoshi = re.findall(r'镶嵌宝石 .+?#', desc)[0].replace('镶嵌宝石 ', '').replace('#', '')
                        if (len(re.findall(r'红玛瑙', baoshi)) > 0):
                            hongmanai = '1'
                        if (len(re.findall(r'太阳石', baoshi)) > 0):
                            taiyangshi = '1'
                        if (len(re.findall(r'舍利子', baoshi)) > 0):
                            shelizi = '1'
                        if (len(re.findall(r'光芒石', baoshi)) > 0):
                            guangmangshi = '1'
                        if (len(re.findall(r'月亮石', baoshi)) > 0):
                            yueliangshi = '1'
                        if (len(re.findall(r'黑宝石', baoshi)) > 0):
                            heibaoshi = '1'
                        if (len(re.findall(r'神秘石', baoshi)) > 0):
                            shenmishi = '1'
                        if (len(re.findall(r'翡翠石', baoshi)) > 0):
                            feicuishi = '1'
                        if (len(re.findall(r'红宝石', baoshi)) > 0 or len(re.findall(r'黄宝石', baoshi)) > 0 or
                            len(re.findall(r'蓝宝石', baoshi)) > 0 or len(re.findall(r'绿宝石', baoshi)) > 0):
                            hongbaoshi = '1'
                    # wrong
                    # baoshi_level = str(each['gem_level'])
                    # baoshi_value = each['gem_value']

                    # baoshi = ''
                    # if (type(baoshi_value) != int):
                    #     for each_baoshi in baoshi_value:
                    #         baoshi += dict_value_to_name[each_baoshi]

                    # if (baoshi_level != '0'):
                    #     if (len(re.findall(r'红玛瑙', baoshi)) > 0):
                    #         hongmanai = '1'
                    #     if (len(re.findall(r'太阳石', baoshi)) > 0):
                    #         taiyangshi = '1'
                    #     if (len(re.findall(r'舍利子', baoshi)) > 0):
                    #         shelizi = '1'
                    #     if (len(re.findall(r'光芒石', baoshi)) > 0):
                    #         guangmangshi = '1'
                    #     if (len(re.findall(r'月亮石', baoshi)) > 0):
                    #         yueliangshi = '1'
                    #     if (len(re.findall(r'黑宝石', baoshi)) > 0):
                    #         heibaoshi = '1'
                    #     if (len(re.findall(r'神秘石', baoshi)) > 0):
                    #         shenmishi = '1'
                    #     if (len(re.findall(r'翡翠石', baoshi)) > 0):
                    #         feicuishi = '1'
                    #     if (len(re.findall(r'红宝石', baoshi)) > 0 or len(re.findall(r'黄宝石', baoshi)) > 0 or
                    #         len(re.findall(r'蓝宝石', baoshi)) > 0 or len(re.findall(r'绿宝石', baoshi)) > 0):
                    #         hongbaoshi = '1'

                    # print(baoshi)
                    # print(baoshi_level)
                    if (len(re.findall(r'星位：', desc)) > 0):
                        xingwei = '1'
                        level_int = int(equip_level_desc)
                        if (level_int > 120):
                            hole_num = '5'
                        elif (level_int > 90):
                            hole_num = '4'
                        elif (level_int > 60):
                            hole_num = '3'
                        else:
                            hole_num = '2'
                    elif (len(re.findall(r'#G开运孔数：.+?#', desc)) > 0):
                        hole_num = re.findall(r'#G开运孔数：.+?#', desc)[0].replace('#G开运孔数：', '').replace('#', '')
                        # print (hole_num)
                        hole_num = re.findall(r'\d孔', desc)[0].replace('孔', '')
                    # print(hole_num)
                    # print(xingwei)

                    temp_text = desc
                    ronglian_begin = desc.find("熔炼效果：")
                    fushi_begin = desc.find("符石:")
                    if fushi_begin > 0 and ronglian_begin < 0:
                            temp_text = temp_text[:fushi_begin]
                    elif fushi_begin > 0 and ronglian_begin > 0:
                        temp_text = temp_text[:fushi_begin] + temp_text[ronglian_begin:]
                    # print ('temp_text:', temp_text)
                    if (len(re.findall(r'防御 \+\d+', temp_text)) > 0):
                        fangyu = re.findall(r'防御 \+\d+', temp_text)[0].replace('防御 +', '')
                        if (len(re.findall(r'\+\d+防御', temp_text)) > 0):
                            fangyu = str(int(fangyu) + int(re.findall(r'\+\d+防御', temp_text)[0].replace('防御', '').replace('+', '')))
                        elif (len(re.findall(r'\-\d+防御', temp_text)) > 0):
                            fangyu = str(int(fangyu) - int(re.findall(r'\-\d+防御', temp_text)[0].replace('防御', '').replace('-', '')))
                        # print ('防御:', fangyu)
                        if kindid == '19':#18.铠甲 59.女衣 17.头盔 58.发钗 19.鞋子 20.腰带 21.饰物'
                            baofangyu = str(int(fangyu) - level_to_xiezi_fangyu[equip_level_desc])
                            # print ('爆防御:', baofangyu)
                        elif kindid == '20':
                            baofangyu = str(int(fangyu) - level_to_yaodai_fangyu[equip_level_desc])
                            # print ('爆防御:', baofangyu)
                    


                        

                    if (len(re.findall(r'气血 \+\d+', temp_text)) > 0):
                        qixue = re.findall(r'气血 \+\d+', temp_text)[0].replace('气血 +', '')
                        # print ('气血1:', qixue)
                        if (len(re.findall(r'\+\d+气血', temp_text)) > 0):
                            qixue = str(int(qixue) + int(re.findall(r'\+\d+气血', temp_text)[0].replace('气血', '').replace('+', '')))
                            # print ('气血2:', qixue)
                        elif (len(re.findall(r'\-\d+气血', temp_text)) > 0):
                            qixue = str(int(qixue) - int(re.findall(r'\-\d+气血', temp_text)[0].replace('气血', '').replace('-', '')))
                            # print ('气血2:', qixue)
                        if kindid == '18' or kindid == '59':#18.铠甲 59.女衣
                            guangmangshijiacheng = qixue
                            guangmangshiduanshu = str(int(int(guangmangshijiacheng) / 40))
                        





                    if (len(re.findall(r'[^G]敏捷 \+\d+', temp_text)) > 0):
                        minjie = re.findall(r'[^G]敏捷 \+\d+', temp_text)[0].replace('敏捷 +', '').replace(' ', '').replace('r', '')
                        # print ('敏捷1:', minjie)
                        if (len(re.findall(r'\+\d+敏捷', temp_text)) > 0):
                            minjie = str(int(minjie) + int(re.findall(r'\+\d+敏捷', temp_text)[0].replace('敏捷', '').replace('+', '')))
                            # print ('敏捷2:', minjie)
                        elif (len(re.findall(r'\-\d+敏捷', temp_text)) > 0):
                            minjie = str(int(minjie) - int(re.findall(r'\-\d+敏捷', temp_text)[0].replace('敏捷', '').replace('-', '')))
                            # print ('敏捷2:', minjie)
                        if kindid == '19':
                            baominjie = str(int(minjie) - level_to_xiezi_minjie[equip_level_desc])
                            # print ('爆敏捷:', baominjie)
                        
                    if (len(re.findall(r'#r伤害 \+\d+', temp_text)) > 0):#G伤害 +24
                        shanghai = re.findall(r'#r伤害 \+\d+', temp_text)[0].replace('#r伤害 +', '')
                        # print ('伤害:', shanghai)
                        if kindid != '17' and kindid != '58':#wuqi
                            baoshanghai = str(int(shanghai) - level_to_wuqi_shanghai[equip_level_desc])
                            # print ('爆伤害:', baoshanghai)
                        else:#toukui17.头盔 58.发钗
                            taiyangshijiacheng = shanghai
                            taiyangshiduanshu = str(int(int(taiyangshijiacheng) / 8))

                    if (len(re.findall(r' 伤害 \+\d+', temp_text)) > 0):#G伤害 +24
                        shanghai = re.findall(r' 伤害 \+\d+', temp_text)[0].replace(' 伤害 +', '')
                        # print ('伤害:', shanghai)
                        if kindid != '17' and kindid != '58':#wuqi
                            baoshanghai = str(int(shanghai) - level_to_wuqi_shanghai[equip_level_desc])
                            # print ('爆伤害:', baoshanghai)
                        else:#toukui17.头盔 58.发钗
                            taiyangshijiacheng = shanghai
                            taiyangshiduanshu = str(int(int(taiyangshijiacheng) / 8))

                    if (len(re.findall(r'#G伤害 \+\d+', temp_text)) > 0):#G伤害 +24
                        shanghai = re.findall(r'#G伤害 \+\d+', temp_text)[0].replace('#G伤害 +', '')
                        # print ('伤害:', shanghai)
                        if kindid != '17' and kindid != '58':#wuqi
                            baoshanghai = str(int(shanghai) - level_to_wuqi_shanghai[equip_level_desc])
                            # print ('爆伤害:', baoshanghai)
                        else:#toukui17.头盔 58.发钗
                            taiyangshijiacheng = shanghai
                            taiyangshiduanshu = str(int(int(taiyangshijiacheng) / 8))


                    if (len(re.findall(r'命中 \+\d+', temp_text)) > 0):
                        mingzhong = re.findall(r'命中 \+\d+', temp_text)[0].replace('命中 +', '')
                        # print ('命中:', mingzhong)
                        if kindid != '17' and kindid != '58':#wuqi
                            baomingzhong = str(int(mingzhong) - level_to_wuqi_mingzhong[equip_level_desc])
                            # print ('爆命中:', baomingzhong)
                        else:#toukui
                            hongmanaijiacheng = mingzhong
                            hongmanaiduanshu = str(int(int(hongmanaijiacheng) / 25))
                    #G法防 +12#
                    if (len(re.findall(r'#G法防 \+\d+', temp_text)) > 0):
                        feicuishijiacheng = re.findall(r'#G法防 \+\d+', temp_text)[0].replace('#G法防 +', '')
                        # print ('法防:', feicuishijiacheng)
                        feicuishiduanshu = str(int(int(feicuishijiacheng) / 12))

                    #G法术吸收率 火+8%、 土+20%#红宝石加成
                    if (len(re.findall(r'#G法术吸收率 .+?#', temp_text)) > 0):
                        xishoulu = 0
                        hongbaoshijiacheng = re.findall(r'#G法术吸收率 .+?#', temp_text)[0].replace('#G法术吸收率', '').replace('#', '')
                        temp_xishou = re.findall(r'\+\d+%', hongbaoshijiacheng)
                        for xishou in temp_xishou:
                            xishoulu += int(xishou.replace('+', '').replace('%', ''))
                        hongbaoshijiacheng = str(xishoulu)
                        # print ('红宝石加成:', hongbaoshijiacheng)
                        hongbaoshiduanshu = str(int(int(hongbaoshijiacheng) / 4))
                    

                    if (len(re.findall(r'速度 \+\d+', temp_text)) > 0):
                        sudu = re.findall(r'速度 \+\d+', temp_text)[0].replace('速度 +', '')
                        # print ('速度:', sudu)
                        heibaoshiduanshu = str(int(int(sudu) / 8))
                    #G躲避 +80#
                    if (len(re.findall(r'#G躲避 \+\d+0#', temp_text)) > 0):
                        duobi = re.findall(r'#G躲避 \+\d+0#', temp_text)[0].replace('躲避 +', '').replace('#', '').replace('G', '')
                        # print ('躲避:', duobi)#duobi == 神秘石加成
                        shenmishiduanshu = str(int(int(duobi) / 20))

                    if (len(re.findall(r'灵力 \+\d+', temp_text)) > 0):
                        lingli = re.findall(r'灵力 \+\d+', temp_text)[0].replace('灵力 +', '')
                        # print ('灵力1:', lingli)
                        if (len(re.findall(r'\+\d+灵力', temp_text)) > 0):
                            lingli = str(int(lingli) + int(re.findall(r'\+\d+灵力', temp_text)[0].replace('灵力', '').replace('+', '')))
                            # print ('灵力2:', lingli)
                        elif (len(re.findall(r'\-\d+灵力', temp_text)) > 0):
                            lingli = str(int(lingli) - int(re.findall(r'\-\d+灵力', temp_text)[0].replace('灵力', '').replace('-', '')))
                            # print ('灵力2:', lingli)
                        if kindid == '21':#饰物
                            sheliziduanshu = str(int(baoshi_level) - int(hongbaoshiduanshu))
                            shelizijiacheng = str(6 * int(sheliziduanshu))
                            baolingli = str(int(lingli) - level_to_xianglian_lingli[equip_level_desc] - int(shelizijiacheng))
                            # print ('爆灵力:', baolingli)
                        elif kindid == '18' or kindid == '59':#18.铠甲 59.女衣
                            shelizijiacheng = lingli
                            sheliziduanshu = str(int(int(shelizijiacheng) / 6))

                    # '体质',
                    if (len(re.findall(r'#G体质 \+\d+', temp_text)) > 0):
                        tizhi = re.findall(r'体质 \+\d+', temp_text)[0].replace('体质 +', '')
                        # print ('体质1:', tizhi)
                        if (len(re.findall(r'\+\d+体质', temp_text)) > 0):
                            tizhi = str(int(tizhi) + int(re.findall(r'\+\d+体质', temp_text)[0].replace('体质', '').replace('+', '')))
                            # print ('体质2:', tizhi)
                        elif (len(re.findall(r'\-\d+体质', temp_text)) > 0):
                            tizhi = str(int(tizhi) - int(re.findall(r'\-\d+体质', temp_text)[0].replace('体质', '').replace('-', '')))
                            # print ('体质2:', tizhi)
                    if (len(re.findall(r'#G体质 \-\d+', temp_text)) > 0):
                        tizhi = re.findall(r'体质 \-\d+', temp_text)[0].replace('体质 ', '')
                        # print ('体质1:', tizhi)
                        if (len(re.findall(r'\+\d+体质', temp_text)) > 0):
                            tizhi = str(int(tizhi) + int(re.findall(r'\+\d+体质', temp_text)[0].replace('体质', '').replace('+', '')))
                            # print ('体质2:', tizhi)
                        elif (len(re.findall(r'\-\d+体质', temp_text)) > 0):
                            tizhi = str(int(tizhi) - int(re.findall(r'\-\d+体质', temp_text)[0].replace('体质', '').replace('-', '')))
                            # print ('体质2:', tizhi)

                    # '耐力',
                    if (len(re.findall(r'#G耐力 \+\d+', temp_text)) > 0):
                        naili = re.findall(r'耐力 \+\d+', temp_text)[0].replace('耐力 +', '')
                        # print ('耐力1:', naili)
                        if (len(re.findall(r'\+\d+耐力', temp_text)) > 0):
                            naili = str(int(naili) + int(re.findall(r'\+\d+耐力', temp_text)[0].replace('耐力', '').replace('+', '')))
                            # print ('耐力2:', naili)
                        elif (len(re.findall(r'\-\d+耐力', temp_text)) > 0):
                            naili = str(int(naili) - int(re.findall(r'\-\d+耐力', temp_text)[0].replace('耐力', '').replace('-', '')))
                            # print ('耐力2:', naili)
                    if (len(re.findall(r'#G耐力 \-\d+', temp_text)) > 0):
                        naili = re.findall(r'耐力 \-\d+', temp_text)[0].replace('耐力 ', '')
                        # print ('耐力1:', naili)
                        if (len(re.findall(r'\+\d+耐力', temp_text)) > 0):
                            naili = str(int(naili) + int(re.findall(r'\+\d+耐力', temp_text)[0].replace('耐力', '').replace('+', '')))
                            # print ('耐力2:', naili)
                        elif (len(re.findall(r'\-\d+耐力', temp_text)) > 0):
                            naili = str(int(naili) - int(re.findall(r'\-\d+耐力', temp_text)[0].replace('耐力', '').replace('-', '')))
                            # print ('耐力2:', naili)
                    # '魔力',
                    if (len(re.findall(r'#G魔力 \+\d+', temp_text)) > 0):
                        moli = re.findall(r'魔力 \+\d+', temp_text)[0].replace('魔力 +', '')
                        # print ('魔力1:', moli)
                        if (len(re.findall(r'\+\d+魔力', temp_text)) > 0):
                            moli = str(int(moli) + int(re.findall(r'\+\d+魔力', temp_text)[0].replace('魔力', '').replace('+', '')))
                            # print ('魔力2:', moli)
                        elif (len(re.findall(r'\-\d+魔力', temp_text)) > 0):
                            moli = str(int(moli) - int(re.findall(r'\-\d+魔力', temp_text)[0].replace('魔力', '').replace('-', '')))
                            # print ('魔力2:', moli)
                    if (len(re.findall(r'#G魔力 \-\d+', temp_text)) > 0):
                        moli = re.findall(r'魔力 \-\d+', temp_text)[0].replace('魔力 ', '')
                        # print ('魔力1:', moli)
                        if (len(re.findall(r'\+\d+魔力', temp_text)) > 0):
                            moli = str(int(moli) + int(re.findall(r'\+\d+魔力', temp_text)[0].replace('魔力', '').replace('+', '')))
                            # print ('魔力2:', moli)
                        elif (len(re.findall(r'\-\d+魔力', temp_text)) > 0):
                            moli = str(int(moli) - int(re.findall(r'\-\d+魔力', temp_text)[0].replace('魔力', '').replace('-', '')))
                            # print ('魔力2:', moli)
                    # '力量'
                    if (len(re.findall(r'#G力量 \+\d+', temp_text)) > 0):
                        liliang = re.findall(r'力量 \+\d+', temp_text)[0].replace('力量 +', '')
                        # print ('力量1:', liliang)
                        if (len(re.findall(r'\+\d+力量', temp_text)) > 0):
                            liliang = str(int(liliang) + int(re.findall(r'\+\d+力量', temp_text)[0].replace('力量', '').replace('+', '')))
                            # print ('力量2:', liliang)
                        elif (len(re.findall(r'\-\d+力量', temp_text)) > 0):
                            liliang = str(int(liliang) - int(re.findall(r'\-\d+力量', temp_text)[0].replace('力量', '').replace('-', '')))
                            # print ('力量2:', liliang)
                    if (len(re.findall(r'#G力量 \-\d+', temp_text)) > 0):
                        liliang = re.findall(r'力量 \-\d+', temp_text)[0].replace('力量 ', '')
                        # print ('力量1:', liliang)
                        if (len(re.findall(r'\+\d+力量', temp_text)) > 0):
                            liliang = str(int(liliang) + int(re.findall(r'\+\d+力量', temp_text)[0].replace('力量', '').replace('+', '')))
                            # print ('力量2:', liliang)
                        elif (len(re.findall(r'\-\d+力量', temp_text)) > 0):
                            liliang = str(int(liliang) - int(re.findall(r'\-\d+力量', temp_text)[0].replace('力量', '').replace('-', '')))
                            # print ('力量2:', liliang)
                    #'敏捷点'
                    if (len(re.findall(r'#G敏捷 \+\d+', temp_text)) > 0):
                        minjiedian = re.findall(r'#G敏捷 \+\d+', temp_text)[0].replace('#G敏捷 +', '')
                        # print ('敏捷点1:', minjiedian)
                        if (len(re.findall(r'\+\d+敏捷', temp_text)) > 0):
                            minjiedian = str(int(minjiedian) + int(re.findall(r'\+\d+敏捷', temp_text)[0].replace('敏捷', '').replace('+', '')))
                            # print ('敏捷点2:', minjiedian)
                        elif (len(re.findall(r'\-\d+敏捷', temp_text)) > 0):
                            minjiedian = str(int(minjiedian) - int(re.findall(r'\-\d+敏捷', temp_text)[0].replace('敏捷', '').replace('-', '')))
                            # print ('敏捷点2:', minjiedian)
                    if (len(re.findall(r'#G敏捷 \-\d+', temp_text)) > 0):
                        minjiedian = re.findall(r'#G敏捷 \-\d+', temp_text)[0].replace('#G敏捷 ', '')
                        # print ('敏捷点1:', minjiedian)
                        if (len(re.findall(r'\+\d+敏捷', temp_text)) > 0):
                            minjiedian = str(int(minjiedian) + int(re.findall(r'\+\d+敏捷', temp_text)[0].replace('敏捷', '').replace('+', '')))
                            # print ('敏捷点2:', minjiedian)
                        elif (len(re.findall(r'\-\d+敏捷', temp_text)) > 0):
                            minjiedian = str(int(minjiedian) - int(re.findall(r'\-\d+敏捷', temp_text)[0].replace('敏捷', '').replace('-', '')))
                            # print ('敏捷点2:', minjiedian)

                    if kindid == '18' or kindid == '59':#18.铠甲 59.女衣
                        temp_duanshu = int(baoshi_level) - int(sheliziduanshu) - int(feicuishiduanshu) - int(guangmangshiduanshu)
                        if temp_duanshu > 0:
                            yueliangshiduanshu = str(temp_duanshu)
                            yueliangshijiacheng = str(12 * temp_duanshu)
                        baofangyu = str(int(fangyu) - level_to_yifu_fangyu[equip_level_desc] - int(yueliangshijiacheng))
                        # print ('爆防御:', baofangyu)
                    if kindid == '17' or kindid == '58':#17.头盔 58.发钗
                        temp_duanshu = int(baoshi_level) - int(taiyangshiduanshu) - int(hongmanaiduanshu)
                        if temp_duanshu > 0:
                            yueliangshiduanshu = str(temp_duanshu)
                            yueliangshijiacheng = str(12 * temp_duanshu)
                        baofangyu = str(int(fangyu) - level_to_toukui_fangyu[equip_level_desc] - int(yueliangshijiacheng))
                        # print ('爆防御:', baofangyu)
                    if kindid == '20':#20.腰带
                        temp_duanshu = int(baoshi_level) - int(shenmishiduanshu) - int(heibaoshiduanshu)
                        if temp_duanshu > 0:
                            guangmangshiduanshu = str(temp_duanshu)
                            guangmangshijiacheng = str(40 * temp_duanshu)
                        baoqixue = str(int(qixue) - level_to_yaodai_qixue[equip_level_desc] - int(guangmangshijiacheng))
                        # print ('爆气血:', baoqixue)



                    #'特技'# #c4DBAF4特技：
                    if (len(re.findall(r'#c4DBAF4特技：', temp_text)) > 0):
                        cut_local = temp_text.find('#c4DBAF4特技：')
                        text_list = re.findall(r'#c4DBAF4[\u4e00-\u9fa5]+', temp_text[cut_local+2:])
                        for text in text_list:
                            text = text.replace('#c4DBAF4', '')
                            if text == '特效' or text == '套装效果':
                                break
                            else:
                                teji += text + ' '
                        teji = teji.strip()
                        # print ('特技:', teji)


            #罗汉金钟 晶清诀 笑里藏刀 破血狂攻 破碎无双 慈航普度 四海升平 玉清诀 放下屠刀 野兽之力 流云诀 凝滞术 光辉之甲 破甲术
            
                        if (len(re.findall(r'罗汉金钟', teji)) > 0):
                            luohanjinzhong = '1'
                        if (len(re.findall(r'晶清诀', teji)) > 0):
                            jingqingjue = '1'
                        if (len(re.findall(r'笑里藏刀', teji)) > 0):
                            xiaolicangdao = '1'
                        if (len(re.findall(r'破血狂攻', teji)) > 0):
                            poxuekuanggong = '1'
                        if (len(re.findall(r'破碎无双', teji)) > 0):
                            posuiwushaung = '1'
                        if (len(re.findall(r'慈航普度', teji)) > 0):
                            cihangpudu = '1'
                        if (len(re.findall(r'四海升平', teji)) > 0):
                            sihaishengping = '1'
                        if (len(re.findall(r'玉清诀', teji)) > 0):
                            yuqingjue = '1'
                        if (len(re.findall(r'放下屠刀', teji)) > 0):
                            fangxiatudao = '1'
                        if (len(re.findall(r'野兽之力', teji)) > 0):
                            yeshouzhili = '1'
                        if (len(re.findall(r'流云诀', teji)) > 0):
                            liuyunjue = '1'
                        if (len(re.findall(r'凝滞术', teji)) > 0):
                            ningzhishu = '1'
                        if (len(re.findall(r'光辉之甲', teji)) > 0):
                            guanghuizhijia = '1'
                        if (len(re.findall(r'破甲术', teji)) > 0):
                            pojiashu = '1'
            #水清诀 弱点击破 聚精会神 燃烧之光 起死回生 回魂咒 圣灵之甲 碎甲术 河东狮吼 魔兽之印 啸风诀 停陷术 先发制人 菩提心佑
                        if (len(re.findall(r'水清诀', teji)) > 0):
                            shuiqingjue = '1'
                        if (len(re.findall(r'弱点击破', teji)) > 0):
                            ruodianjipo = '1'
                        if (len(re.findall(r'聚精会神', teji)) > 0):
                            jujinghuishen = '1'
                        if (len(re.findall(r'燃烧之光', teji)) > 0):
                            ranshaozhiguang = '1'
                        if (len(re.findall(r'起死回生', teji)) > 0):
                            qisihuisheng = '1'
                        if (len(re.findall(r'回魂咒', teji)) > 0):
                            huihunzhou = '1'
                        if (len(re.findall(r'圣灵之甲', teji)) > 0):
                            shenglingzhijia = '1'
                        if (len(re.findall(r'碎甲术', teji)) > 0):
                            suijiashu = '1'
                        if (len(re.findall(r'河东狮吼', teji)) > 0):
                            hedongshihou = '1'
                        if (len(re.findall(r'魔兽之印', teji)) > 0):
                            moshouzhiyin = '1'
                        if (len(re.findall(r'啸风诀', teji)) > 0):
                            xiaofengjue = '1'
                        if (len(re.findall(r'停陷术', teji)) > 0):
                            tingxianshu = '1'
                        if (len(re.findall(r'先发制人', teji)) > 0):
                            xianfazhiren = '1'
                        if (len(re.findall(r'菩提心佑', teji)) > 0):
                            putixinyou = '1'
            # 吸血 残月 命归术 虚空之刃 气疗术 心疗术 命疗术 凝气诀 凝神决 气归术 冰清诀 诅咒之伤 诅咒之亡 绝幻魔音 太极护法
                        if (len(re.findall(r'吸血', teji)) > 0):
                            xixue = '1'
                        if (len(re.findall(r'残月', teji)) > 0):
                            canyue = '1'
                        if (len(re.findall(r'命归术', teji)) > 0):
                            mingguishu = '1'
                        if (len(re.findall(r'虚空之刃', teji)) > 0):
                            xukongzhiren = '1'
                        if (len(re.findall(r'气疗术', teji)) > 0):
                            qiliaoshu = '1'
                        if (len(re.findall(r'心疗术', teji)) > 0):
                            xinliaoshu = '1'
                        if (len(re.findall(r'命疗术', teji)) > 0):
                            mingliaoshu = '1'
                        if (len(re.findall(r'凝气诀', teji)) > 0):
                            ningqijue = '1'
                        if (len(re.findall(r'凝神决', teji)) > 0):
                            ningshenjue = '1'
                        if (len(re.findall(r'气归术', teji)) > 0):
                            qiguishu = '1'
                        if (len(re.findall(r'冰清诀', teji)) > 0):
                            bingqingjue = '1'
                        if (len(re.findall(r'诅咒之伤', teji)) > 0):
                            zuzhouzhishang = '1'
                        if (len(re.findall(r'诅咒之亡', teji)) > 0):
                            zuzhouzhiwang = '1'
                        if (len(re.findall(r'绝幻魔音', teji)) > 0):
                            juehuanmoyin = '1'
                        if (len(re.findall(r'太极护法', teji)) > 0):
                            taijihufa = '1'
            # 修罗咒 天衣无缝 冥王暴杀 乾坤斩 帝释无双 伽罗无双 亡灵之刃 死亡之音 身似菩提 心如明镜 移形换影 凝心决 毁灭之光 金刚不坏
                        if (len(re.findall(r'修罗咒', teji)) > 0):
                            xiuluozhou = '1'
                        if (len(re.findall(r'天衣无缝', teji)) > 0):
                            tianyiwufeng = '1'
                        if (len(re.findall(r'冥王暴杀', teji)) > 0):
                            mingwangbaosha = '1'
                        if (len(re.findall(r'乾坤斩', teji)) > 0):
                            qiankunzhan = '1'
                        if (len(re.findall(r'帝释无双', teji)) > 0):
                            dishiwushuang = '1'
                        if (len(re.findall(r'伽罗无双', teji)) > 0):
                            jialuowushuang = '1'
                        if (len(re.findall(r'亡灵之刃', teji)) > 0):
                            wanglingzhiren = '1'
                        if (len(re.findall(r'死亡之音', teji)) > 0):
                            siwangzhiyin = '1'
                        if (len(re.findall(r'身似菩提', teji)) > 0):
                            shensiputi = '1'
                        if (len(re.findall(r'心如明镜', teji)) > 0):
                            xinrumingjing = '1'
                        if (len(re.findall(r'移形换影', teji)) > 0):
                            yixinghuanying = '1'
                        if (len(re.findall(r'凝心决', teji)) > 0):
                            ningxinjue = '1'
                        if (len(re.findall(r'毁灭之光', teji)) > 0):
                            huimiezhiguang = '1'
                        if (len(re.findall(r'金刚不坏', teji)) > 0):
                            jingangbuhuai = '1'


                    #'特效'
                    # #c4DBAF4特效：
                    if (len(re.findall(r'#c4DBAF4特效：', temp_text)) > 0):
                        cut_local = temp_text.find('#c4DBAF4特效：')
                        text_list = re.findall(r'#c4DBAF4[\u4e00-\u9fa5]+', temp_text[cut_local+2:])
                        for text in text_list:
                            text = text.replace('#c4DBAF4', '')
                            if text == '特技' or text == '套装效果':
                                break
                            else:
                                texiao += text + ' '
                        texiao = texiao.strip()
                        # print ('特效:', texiao)
                        if (len(re.findall(r'无级别限制', texiao)) > 0):
                            wujibie = '1'
                        if (len(re.findall(r'愤怒', texiao)) > 0):
                            fennu = '1'
                        if (len(re.findall(r'永不磨损', texiao)) > 0):
                            bumo = '1'
                        if (len(re.findall(r'简易', texiao)) > 0):
                            jianyi = '1'
                        if (len(re.findall(r'暴怒', texiao)) > 0):
                            baonu = '1'
                        if (len(re.findall(r'神农', texiao)) > 0):
                            shennong = '1'
                        if (len(re.findall(r'神佑', texiao)) > 0):
                            shenyou = '1'
                        if (len(re.findall(r'精致', texiao)) > 0):
                            jingzhi = '1'
                        if (len(re.findall(r'绝杀', texiao)) > 0):
                            juesha = '1'
                        if (len(re.findall(r'专注', texiao)) > 0):
                            zhuanzhu = '1'
                        if (len(re.findall(r'必中', texiao)) > 0):
                            bizhong = '1'


                    # #c4DBAF4套装效果：
                    if (len(re.findall(r'#c4DBAF4套装效果：[\u4e00-\u9fa5]+', temp_text)) > 0):
                        taozhuang = re.findall(r'#c4DBAF4套装效果：[\u4e00-\u9fa5]+', temp_text)[0].replace('#c4DBAF4套装效果：', '')
                        # print ('套装效果:', taozhuang)
                    if (len(re.findall(r'#c4DBAFF[^\\u]+?#', temp_text)) > 0):
                        zhuangbeitexing_wanzheng = re.findall(r'#c4DBAFF[^\\u]+?#', temp_text)[0].replace('#c4DBAFF', '').replace('#', '')
                        zhuangbeitexing = re.findall(r'[\u4e00-\u9fa5]+', zhuangbeitexing_wanzheng)[0]
                        # print ('160级装备特性:', zhuangbeitexing)

                    #new json method
                    init_defense = str(each['init_defense'])#初防

                    init_dex = str(each['init_dex'])#初敏

                    init_wakan = str(each['init_wakan'])#初灵

                    init_damage_raw = str(each['init_damage_raw'])#初伤（不含命中）

                    init_damage = str(each['init_damage'])#初伤（包含命中

                    all_damage = str(each['all_damage'])#总伤

                    init_hp = str(each['init_hp'])#初血

                    addon_lingli = str(each['addon_lingli'])#若在衣服上打了舍利子，这里表示舍利子加的灵力

                except(Exception) as ex:
                    print('error:',ex)
                    # print ('each:', each)
                    continue
                #xieru csv
                writer.writerow({'equip_level':equip_level_desc,'price_int':price_int,'server_id': server_id, 
                    'hole_num':hole_num, 'kindid':kindid, '人造': renzao, '失败次数': failtime,
                    'equip_name': equip_name, '锻炼等级': baoshi_level, '镶嵌宝石': baoshi, 
                    '红玛瑙': hongmanai, '太阳石': taiyangshi, '舍利子': shelizi, '光芒石': guangmangshi, '月亮石': yueliangshi,
                    '黑宝石': heibaoshi, '神秘石': shenmishi, '翡翠石': feicuishi,'红宝石': hongbaoshi, 
                    '初伤（包含命中）': init_damage, '初伤（不含命中）': init_damage_raw, '初防': init_defense, '初血': init_hp, '初敏': init_dex, '初灵': init_wakan, '总伤': all_damage,
                    '红玛瑙加成': hongmanaijiacheng,
                    '太阳石加成': taiyangshijiacheng, '舍利子加成': shelizijiacheng, '光芒石加成': guangmangshijiacheng,
                    '月亮石加成': yueliangshijiacheng, '翡翠石加成': feicuishijiacheng,
                    '红宝石加成': hongbaoshijiacheng,
                    '红玛瑙段数': hongmanaiduanshu, '太阳石段数': taiyangshiduanshu, '舍利子段数': sheliziduanshu,
                    '光芒石段数': guangmangshiduanshu, '月亮石段数': yueliangshiduanshu, '黑宝石段数': heibaoshiduanshu,
                    '神秘石段数': shenmishiduanshu, '翡翠石段数': feicuishiduanshu, '红宝石段数': hongbaoshiduanshu,
                    '星位': xingwei, '伤害': shanghai, '爆伤害': baoshanghai, '命中': mingzhong, '爆命中': baomingzhong, '防御': fangyu, '爆防御': baofangyu, '气血': qixue, '爆气血': baoqixue, '躲避': duobi,
                    '灵力': lingli, '爆灵力': baolingli, '敏捷': minjie, '爆敏捷': baominjie,'敏捷点': minjiedian, '速度': sudu, '体质': tizhi, '耐力': naili,
                    '魔力': moli, '力量': liliang, '特技': teji, '罗汉金钟': luohanjinzhong, '晶清诀': jingqingjue, '笑里藏刀': xiaolicangdao, '破血狂攻': poxuekuanggong, '破碎无双': posuiwushaung, '慈航普度': cihangpudu, '四海升平': sihaishengping, '玉清诀': yuqingjue,
                    '放下屠刀': fangxiatudao, '野兽之力': yeshouzhili, '流云诀': liuyunjue, '凝滞术': ningzhishu, '光辉之甲': guanghuizhijia, '破甲术': pojiashu, '水清诀': shuiqingjue, '弱点击破': ruodianjipo, '聚精会神': jujinghuishen, '燃烧之光': ranshaozhiguang,
                    '起死回生': qisihuisheng, '回魂咒': huihunzhou, '圣灵之甲': shenglingzhijia, '碎甲术': suijiashu, '河东狮吼': hedongshihou, '魔兽之印': moshouzhiyin, '啸风诀': xiaofengjue, '停陷术': tingxianshu, '先发制人': xianfazhiren, '菩提心佑': putixinyou,
                    '吸血': xixue, '残月': canyue, '命归术': mingguishu, '虚空之刃': xukongzhiren, '气疗术': qiliaoshu, '心疗术': xinliaoshu, '命疗术': mingliaoshu, '凝气诀': ningqijue, '凝神决': ningshenjue, '气归术': qiguishu, '冰清诀': bingqingjue,
                    '诅咒之伤': zuzhouzhishang, '诅咒之亡': zuzhouzhiwang, '绝幻魔音': juehuanmoyin, '太极护法': taijihufa, '修罗咒': xiuluozhou, '天衣无缝': tianyiwufeng, '冥王暴杀': mingwangbaosha, '乾坤斩': qiankunzhan, '帝释无双': dishiwushuang, '伽罗无双': jialuowushuang,
                    '亡灵之刃': wanglingzhiren, '死亡之音': siwangzhiyin, '身似菩提': shensiputi, '心如明镜': xinrumingjing, '移形换影': yixinghuanying, '凝心决': ningxinjue, '毁灭之光': huimiezhiguang, '金刚不坏': jingangbuhuai,'特效': texiao, '无级别': wujibie, '愤怒': fennu, '永不磨损': bumo,
                    '简易': jianyi, '暴怒': baonu, '神农': shennong, '神佑': shenyou, '精致': jingzhi, '绝杀': juesha,
                    '专注': zhuanzhu, '必中': bizhong, '套装效果': taozhuang, '160级装备特性': zhuangbeitexing})
                # print ("\n\n")
        print ('%dof%d,已爬取%s, %s, %d页' %(server_count, server_sum, server_name, kindid_to_name[kindid], total_pages))    
        fp.close()
        time.sleep(200+random.randint(1,50))    #每次爬取完一个服务器之后，暂停200秒再开始爬取下一个。

if __name__ == '__main__' :
    main()
