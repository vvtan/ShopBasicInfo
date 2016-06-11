# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
from scrapy.conf import settings
import re
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ShopBasicInfoPipeline(object):
    def __init__(self):
        self.host = os.getenv('POSTGRESQL_HOST')
        self.port = os.getenv('POSTGRESQL_PORT')
        self.user = os.getenv('POSTGRESQL_USER')
        self.password = os.getenv('POSTGRESQL_PASSWORD')
        self.database = os.getenv('POSTGRESQL_DATABASE')

    def process_item(self, item, spider):
        add_time = self.format_info(item['add_time'])
        modify_time = self.format_info(item['modify_time'])
        nick = self.format_info(item['nick'])
        shop_type = self.format_info(item['shop_type'])
        shop_name = self.format_info(item['shop_name'])
        shop_id = self.format_info(item['shop_id'])
        shop_address_province = self.format_info(item['shop_address_province'])
        shop_address_city = self.format_info(item['shop_address_city'])
        total_sold = self.format_info(item['total_sold'])
        goods_number = self.format_info(item['goods_number'])
        good_rate_percent = self.format_info(item['good_rate_percent'])
        shop_img_url = self.format_info(item['shop_img_url'])
        shop_rate_url = self.format_info(item['shop_rate_url'])
        main_business = self.format_info(item['main_business'])
        deposit = self.format_info(item['deposit'])
        seller_rank = self.format_info(item['seller_rank'])
        buyer_rank = self.format_info(item['buyer_rank'])
        main_rate = self.format_info(item['main_rate'])
        is_exist = self.format_info(item['is_exist'])
        shop_label = item['shop_label']
        print nick
        print shop_label
        self.conn = psycopg2.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        self.cursor = self.conn.cursor()
        sql = 'insert into shop_basic(add_time,modify_time,nick,shop_type,shop_name,shop_id,shop_address_province, shop_address_city, total_sold,goods_number,good_rate_percent,shop_img_url,shop_rate_url,main_business,deposit,seller_rank,buyer_rank,main_rate,is_exist) \
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        data = (
            add_time, modify_time, nick, shop_type, shop_name, shop_id, shop_address_province, shop_address_city,
            total_sold, goods_number, good_rate_percent, shop_img_url, shop_rate_url, main_business, deposit,
            seller_rank, buyer_rank, main_rate, is_exist)
        try:
            self.cursor.execute(sql, data)
            if shop_label != '':
                sql1 = 'insert into shop_basic_label(add_time,modify_time,nick,shop_label) values(%s,%s,%s,%s)'
                shop_label_s = str(shop_label).split(',')
                for shop_label in shop_label_s:
                    data1 = (add_time, modify_time, nick, shop_label)
                    self.cursor.execute(sql1, data1)
            self.conn.commit()
        except Exception as e:
            print e
            self.conn.rollback()
            self.cursor = self.conn.cursor()
            sql = 'update  shop_basic set modify_time=%s, shop_type=%s, shop_name=%s, shop_id=%s, shop_address_province=%s, shop_address_city=%s, total_sold=%s, goods_number=%s, good_rate_percent=%s, shop_img_url=%s, shop_rate_url=%s, main_business=%s, deposit=%s, seller_rank=%s, buyer_rank=%s, main_rate=%s, is_exist=%s' \
                  ' where nick = %s'
            data = (
                modify_time, shop_type, shop_name, shop_id, shop_address_province, shop_address_city,
                total_sold, goods_number, good_rate_percent, shop_img_url, shop_rate_url, main_business, deposit,
                seller_rank, buyer_rank, main_rate, is_exist, nick)
            self.cursor.execute(sql, data)
            sql2 = 'delete from shop_basic_label where nick = \'%s\'' % nick
            self.cursor.execute(sql2)
            if shop_label != '':
                sql1 = 'insert into shop_basic_label(add_time,modify_time,nick,shop_label) values(%s,%s,%s,%s)'
                shop_label_s = str(shop_label).split(',')
                for shop_label in shop_label_s:
                    data1 = (add_time, modify_time, nick, shop_label)
                    self.cursor.execute(sql1, data1)
        finally:
            # print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
            self.cursor.close()
            self.conn.commit()
            self.conn.close()
        print(nick)
        print(shop_type)
        print(shop_name)
        print(shop_id)
        print(total_sold)
        print(goods_number)
        print(shop_label)
        print(good_rate_percent)
        print(shop_img_url)
        print(shop_rate_url)
        print(main_business)

        return item

    def format_info(self, content):
        if isinstance(content, str):
            return str(content).strip()
        else:
            return content