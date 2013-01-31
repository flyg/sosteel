from scraper.items import SteelItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

class UsteelSpider(CrawlSpider):
    name = "zhaogang"
    allowed_domains = ["www.zhaogang.com"]
    start_urls = ["http://www.zhaogang.com/spot/"]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/spot/\b', )), callback = 'parse_item', follow = True),
        Rule(SgmlLinkExtractor(allow=('/spot/\?page=[0..9]*', )), callback = 'parse_item', follow = True),
        )

    def parse_base(self, response):
        hxs = HtmlXPathSelector(response)
        webItems = hxs.select('//*//table[@class="table"]/tbody/tr')
        objects = [];
        for webItem in webItems:
            if (webItem.select('./td').__len__() >= 9):
                object = SteelItem()
                nameObject                  = webItem.select('./td[1]/div/span/a/text()')
                if (nameObject.__len__() > 0):
                    object['name']          = nameObject.extract()[0]
                object['url']               = webItem.select('./td[9]/div/a/@href').extract()[0]
                object['model']             = webItem.select('./td[3]/a/text()').extract()[0]
                object['size']              = webItem.select('./td[2]/a/text()').extract()[0]
                producerObject              = webItem.select('./td[4]/a/text()')
                if (producerObject.__len__() > 0):
                    object['producer']      = producerObject.extract()[0]
                stockLocationObject         = webItem.select('./td[5]/text()')
                if (stockLocationObject.__len__() > 0):
                    object['stock_location']= stockLocationObject.extract()[0]
                object['price']             = webItem.select('./td[7]/text()').extract()[0]
                object['stock']             = webItem.select('./td[6]/text()').extract()[0]
                object['reseller']          = webItem.select('./td[8]/text()').extract()[0]
                objects.append(object)
        return objects

    def parse_start_url(self, response):
        self.parse_base(response)

    def parse_item(self, response):
        self.parse_base(response)