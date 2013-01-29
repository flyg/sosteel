# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class SteelItem(Item):
    name = Field()
    url = Field()
    model = Field()
    size = Field()
    stock = Field()
    price = Field()
    producer = Field()
    producer_location = Field()
    stock_location = Field()
    reseller = Field()
    reseller_location = Field()
    date = Field()

