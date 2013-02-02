from scraper.items import SteelItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
import time
import string

class OpsteelSpider(CrawlSpider):
    name = "opsteel"
    allowed_domains = ["www.opsteel.cn"]
    start_urls = ["http://www.opsteel.cn/quote/"]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/quote/\b', )), callback = 'parse_item', follow = True),
        Rule(SgmlLinkExtractor(allow=('/quote/[0-9]*.html', )), callback = 'parse_item', follow = True),
    )

    def parse_base(self, response):
        time.sleep(0.1)
        hxs = HtmlXPathSelector(response)
        webItems = hxs.select('//*//div[@id="result-bd"]//table[@class="tb-pro tb-list"]/tbody/tr')
        objects = [];
        for webItem in webItems:
            object = SteelItem()
            object['name']              = string.join(webItem.select('./td[1]/a/text()').extract(), "")
            object['url']               = "http://www.opsteel.cn" + string.join(webItem.select('./td[1]/a/@href').extract(), "")
            object['model']             = string.join(webItem.select('./td[3]/text()').extract(), "")
            object['size']              = string.join(webItem.select('./td[2]/text()').extract(), "")
            object['producer']          = string.join(webItem.select('./td[4]/text()').extract(), "")
            object['producer_location'] = string.join(webItem.select('./td[5]/text()').extract(), "")
            object['stock_location']    = string.join(webItem.select('./td[6]/text()').extract(), "")
            object['price']             = string.join(webItem.select('./td[8]/strong/text()').extract(), "")
            object['stock']             = string.join(webItem.select('./td[7]/text()').re(r'\r\n\t*(.*)\r\n\t*'), "")
            object['reseller']          = string.join(webItem.select('./td[9]/div/a/text()').extract(), "")
            objects.append(object)
        return objects

    def parse_start_url(self, response):
        return self.parse_base(response)

    def parse_item(self, response):
        return self.parse_base(response)