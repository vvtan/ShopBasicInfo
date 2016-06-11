# -*- coding: utf-8 -*-
import re
import datetime
import requests
import json
import urllib
from scrapy_redis.spiders import RedisSpider
from ShopBasicInfo.items import ShopbasicinfoItem
from scrapy_redis import connection
from scrapy.conf import settings
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ShopBasicInfoSpider(RedisSpider):
    name = "shop_basic_info"
    start_urls = [
        ]
    redis_server = connection.from_settings(settings)

    def parse(self, response):
        head = {'User-Agent': \
                    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
                'cookie': 'cna=9dmhD/z0ODgCATHd1PgOvAEo; ali_ab=49.221.212.248.1461498199870.2; hng=CN%7Czh-cn%7CCNY; thw=cn; isg=0402F5E80881A216E6813A6676800CB8; v=0; _tb_token_=ku02IolX76m3jJ; uc1=cookie14=UoWxMP74ys3MPA%3D%3D&existShop=false&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=VFC%2FuZ9aiKCaj7AzN6nc&tag=1&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=sg2=UIS5OL%2BOEDgy%2FIeQ7IgTu7dSOvuG0LEay5288ZRYw64%3D&nk2=pbEaPGpOBJk%3D&id2=UoYfobtYhLxhEw%3D%3D&vt3=F8dASmgu7PcOeAskyes%3D&lg2=UtASsssmOIJ0bQ%3D%3D; existShop=MTQ2MTkyMDU3MA%3D%3D; uss=UIIpyK78%2BArm1rQcpUrk%2FRwXHQDc93OpxAQgdlu7DWHJVDuJuqKSxy5hBg%3D%3D; lgc=%5Cu4F01%5Cu513F%5Cu8469%5Cu8469; tracknick=%5Cu4F01%5Cu513F%5Cu8469%5Cu8469; cookie2=1cd8c28594101548f03793d63c556c34; sg=%E8%91%A937; mt=np=&ci=9_1&cyk=-1_-1; cookie1=Vvkh3e1O2MWb%2FWoyF7KMYkHR3r9XP1ItH8ivkdLbbCM%3D; unb=1710468073; skt=6e1a6a704a8e0ddd; t=a74cdfe08cedf1981150320f20e9a793; _cc_=U%2BGCWk%2F7og%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu4F01%5Cu513F%5Cu8469%5Cu8469; cookie17=UoYfobtYhLxhEw%3D%3D; l=Av7-AatB1kluKMPP1QNNkk-Bzh5BL8LA'
                }
        seller_nick = urllib.unquote(re.search('&q=(.*?)&', response.url + '&').group(1)).decode('utf-8')
        print seller_nick
        html = response.body
        content = re.search('g_page_config = (.*?);\n', html, re.S)
        while not content:
            html = requests.get(response.url, headers=head).text
            content = re.search('g_page_config = (.*?);\n', html, re.S)
        content = content.group(1)
        # 解析出全部店铺列表信息的json
        data = json.loads(content).get('mods').get('shoplist').get('data')
        # 判断搜索有没有结果
        if data is not None:
            the_shop_data = data.get('shopItems')[0]
            nick = the_shop_data.get('nick')
            # 第一个店铺的nick要跟给定的nick相等
            if nick == seller_nick:
                shop_type = the_shop_data.get('shopIcon').get('iconClass').strip()
                shop_name = the_shop_data.get('rawTitle').strip()
                shop_id = the_shop_data.get('nid').strip()
                shop_address = the_shop_data.get('provcity').strip()
                total_sold = int(the_shop_data.get('totalsold'))
                goods_number = int(the_shop_data.get('procnt'))
                shop_label = ''
                icons = the_shop_data.get('icons')
                for i in icons:
                    shop_label = shop_label + i.get('title') + ','
                if len(shop_label) > 0:
                    shop_label = shop_label[:-1]
                good_rate_percent = float(self.delete_the_percent(the_shop_data.get('goodratePercent')))
                shop_img_url = the_shop_data.get('picUrl').strip()
                shop_rate_url = the_shop_data.get('userRateUrl').strip()
                dsrStr = json.loads(the_shop_data.get('dsrInfo').get('dsrStr'))
                main_business = dsrStr.get('ind').strip()
                if main_business == '':
                    main_business = None

                describe_score_industry = self.delete_the_percent(dsrStr.get('mg'))
                service_score_industry = self.delete_the_percent(dsrStr.get('sg'))
                logistics_score_industry = self.delete_the_percent(dsrStr.get('cg'))


                # 判断店铺等级是否为0
                if shop_type != 'rank seller-rank-0':
                    url = 'https:' + shop_rate_url
                    html = requests.get(url, headers=head)
                    add_time = datetime.datetime.today()
                    modify_time = add_time

                    is_exist = True
                    deposit = None
                    seller_rank = None
                    buyer_rank = None
                    main_rate = None
                    # 切割地址
                    if shop_address != '':
                        shop_address_s = str(shop_address).split(' ')
                        if len(shop_address_s) == 2:
                            shop_address_province = shop_address_s[0]
                            shop_address_city = shop_address_s[1]
                        elif len(shop_address_s) == 1:
                            shop_address_province = shop_address_s[0]
                            shop_address_city = None
                    else:
                        shop_address_province = None
                        shop_address_city = None
                    if shop_type != 'icon-service-tianmao-large':
                        if shop_type == 'icon-service-qiye-large':
                            shop_type = '企业店铺'
                        else:
                            shop_type = '普通店铺'
                    else:
                        shop_type = '天猫店铺'


                    item = ShopbasicinfoItem()
                    item['add_time'] = add_time
                    item['modify_time'] = modify_time
                    item['nick'] = nick
                    item['shop_type'] = shop_type
                    item['shop_name'] = shop_name
                    item['shop_id'] = shop_id
                    item['shop_address_province'] = shop_address_province
                    item['shop_address_city'] = shop_address_city
                    item['total_sold'] = total_sold
                    item['goods_number'] = goods_number
                    item['good_rate_percent'] = good_rate_percent
                    item['shop_img_url'] = shop_img_url
                    item['shop_rate_url'] = shop_rate_url
                    item['main_business'] = main_business
                    item['deposit'] = deposit
                    item['seller_rank'] = seller_rank
                    item['buyer_rank'] = buyer_rank
                    item['main_rate'] = main_rate
                    item['is_exist'] = is_exist
                    item['shop_label'] = shop_label

                    yield item



    def getContent(self,content):
        if content:
            return content[0]
        return None

    def getNumber(self,content):
        if content:
            result = re.search('(\d+)', content[0])
            if result:
                return float(result.group(1))
        return 0

    def getUserId(self,content):
        content = re.search('"userID": "(.*?)"', content)
        if content:
            return content.group(1)
        return None

    def getCharge(self,content):
        content = re.search('￥(.*)', self.getContent(content))
        if content:
            return float(content.group(1).replace(',', ''))
        return 0

    def delete_the_percent(self,content):
        if content:
            content = re.search('(.*)%', content)
        if content:
            print('###' + content.group(1))
            return float(content.group(1))
        return 0

    def delete_the_fen(self,content):
        if content:
            content = re.search('(.*)分', content)
        if content:
            print('fen' + content.group(1))
            return float(content.group(1))
        return 0

    def delete_the_tian(self,content):
        if content:
            content = re.search('(.*)天', content)
        if content:
            print('天' + content.group(1))
            return float(content.group(1))
        return 0

