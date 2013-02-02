# -*- coding=UTF-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class SteelItem(Item):
    model = Field()             #品名
    url = Field()               #原链接
    trademark = Field()         #牌号
    spec = Field()              #规格
    weight = Field()            #总重
    price = Field()             #价格
    producer = Field()
    origin = Field()            #产地
    stock_location = Field()    #仓库
    provider = Field()          #供应商
    date = Field()







