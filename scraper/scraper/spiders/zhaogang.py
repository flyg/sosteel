from scraper.items import SteelItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
import string

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
                object['name']              = string.join(webItem.select('./td[1]/div/span/a/text()').extract(), "")
                object['url']               = string.join(webItem.select('./td[9]/div/a/@href').extract(), "")
                object['model']             = string.join(webItem.select('./td[3]/a/text()').extract(), "")
                object['size']              = string.join(webItem.select('./td[2]/a/text()').extract(), "")
                object['producer']          = string.join(webItem.select('./td[4]/a/text()').extract(), "")
                object['stock_location']    = string.join(webItem.select('./td[5]/text()').extract(), "")
                object['price']             = string.join(webItem.select('./td[7]/text()').extract(), "")
                object['stock']             = string.join(webItem.select('./td[6]/text()').extract(), "")
                object['reseller']          = string.join(webItem.select('./td[8]/text()').extract(), "")
                objects.append(object)
        return objects

    def parse_start_url(self, response):
        return self.parse_base(response)

    def parse_item(self, response):
        return self.parse_base(response)