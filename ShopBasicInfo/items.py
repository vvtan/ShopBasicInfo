# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopbasicinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    add_time = scrapy.Field()
    modify_time = scrapy.Field()
    nick = scrapy.Field()
    shop_type = scrapy.Field()
    shop_name = scrapy.Field()
    shop_id = scrapy.Field()
    shop_address_province = scrapy.Field()
    shop_address_city = scrapy.Field()
    total_sold = scrapy.Field()
    goods_number = scrapy.Field()
    good_rate_percent = scrapy.Field()
    shop_img_url = scrapy.Field()
    shop_rate_url = scrapy.Field()
    main_business = scrapy.Field()
    deposit = scrapy.Field()
    seller_rank = scrapy.Field()
    buyer_rank = scrapy.Field()
    main_rate = scrapy.Field()
    is_exist = scrapy.Field()
    shop_label = scrapy.Field()
