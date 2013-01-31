from scraper.items import SteelItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

class UsteelSpider(CrawlSpider):
    name = "usteel"
    allowed_domains = ["shop.usteel.com"]
    start_urls = ["http://shop.usteel.com/index.php?app=gangcai"]

    rules = (
        Rule(SgmlLinkExtractor(allow = ('index.php\?app=gangcai', ), deny = ('id=', )), callback = 'parse_item', follow = True),
        Rule(SgmlLinkExtractor(allow = ('index.php\?app=buxiu', ), deny = ('id=', )), callback = 'parse_item', follow = True),
    )

    def parse_base(self, response):
        hxs = HtmlXPathSelector(response)
        webItems = hxs.select('//*//div[@class="result mb10"]//ul[@class="list"]/li')
        objects = [];
        for webItem in webItems:
            object = SteelItem()
            object['name']              = webItem.select('*/span[@class="s1 textL"]/a/@title').extract()[0]
            object['url']               = "http://shop.usteel.com/" + webItem.select('*/span[@class="s1 textL"]/a/@href').extract()[0]
            object['model']             = webItem.select('*/span[@class="s2"]/text()').extract()[0]
            object['size']              = webItem.select('*/span[@class="s3"]/text()').extract()[0]
            object['producer']          = webItem.select('*/span[@class="s4"]/text()').extract()[0]
            object['producer_location'] = webItem.select('*/span[@class="s5"]/text()').extract()[0]
            object['price']             = webItem.select('*/span[@class="s6"]/b/text()').extract()[0]
            object['stock']             = webItem.select('*/span[@class="s6"]/i/text()').extract()[0]
            object['reseller']          = webItem.select('*/span[@class="s8 textL"]/a/@title').extract()[0]
            objects.append(object)
        return objects

    def parse_start_url(self, response):
        self.parse_base(response)

    def parse_item(self, response):
        self.parse_base(response)