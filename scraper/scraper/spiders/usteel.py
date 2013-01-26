from scraper.items import SteelItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

class UsteelSpider(CrawlSpider):
    name = "usteel"
    allowed_domains = ["shop.usteel.com"]
    start_urls = ["http://shop.usteel.com/index.php?app=gangcai"]

    rules = (
        Rule(SgmlLinkExtractor(allow=('index.php', )), callback = 'parse_item'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        webItems = hxs.select('//*//div[@class="result mb10"]//ul[@class="list"]')
        objects = [];
        for webItem in webItems:
            object = SteelItem()
            object['name']              = webItem.select('//span[@class="s1 textL"]/a/@title').extract()
            object['model']             = webItem.select('//span[@class="s2"]/text()').extract()
            object['size']              = webItem.select('//span[@class="s3"]/text()').extract()
            object['producer']          = webItem.select('//span[@class="s4"]/text()').extract()
            object['producer_location'] = webItem.select('//span[@class="s5"]/text()').extract()
            object['price']             = webItem.select('//span[@class="s6"]/b/text()').extract()
            object['stock']             = webItem.select('//span[@class="s6"]/i/text()').extract()
            object['reseller']          = webItem.select('//span[@class="s8 textL"]/a/@title').extract()
            objects.append(object)
        return objects
