from scraper.items import SteelItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
import string
import json

class UsteelSpider(CrawlSpider):
    name = "511steel"
    allowed_domains = ["www.511steel.com"]
    start_urls = ["http://www.511steel.com/Customer/Resource/Ajax/ResourceGet.ashx?op=searchkk&data=%3CRoot%3E%3CPz%3E%3C/Pz%3E%3CCd%3E%3C/Cd%3E%3CCk%3E%3C/Ck%3E%3CMinPrice%3E%3C/MinPrice%3E%3CMaxPrice%3E%3C/MaxPrice%3E%3CPh%3E%3C/Ph%3E%3CMinThickness%3E%3C/MinThickness%3E%3CMaxThickness%3E%3C/MaxThickness%3E%3CMinWidth%3E%3C/MinWidth%3E%3CMaxWidth%3E%3C/MaxWidth%3E%3CMinLength%3E%3C/MinLength%3E%3CMaxLength%3E%3C/MaxLength%3E%3CRows%3E20%3C/Rows%3E%3C/Root%3E&t=1359866430453&_=1359866430466&sEcho=1&iColumns=14&sColumns=&iDisplayStart=0&iDisplayLength=20000"]

    rules = (
        Rule(SgmlLinkExtractor(allow=('', )), callback = 'parse_item', follow = True),
        )

    def parse_base(self, response):
        body = response.body
        data = json.loads(body)
        webItems = data['aaData']
        objects = [];
        for webItem in webItems:
            object = SteelItem()
            object['url']               = "http://www.511steel.com/Customer/Resource/Purchase.aspx"
            hxs = HtmlXPathSelector(text = webItem[1])
            object['model']             = string.join(hxs.select('*/div/text()').extract(), "")
            hxs = HtmlXPathSelector(text = webItem[2])
            object['trademark']         = string.join(hxs.select('*/div/text()').extract(), "")
            hxs = HtmlXPathSelector(text = webItem[3])
            object['spec']              = string.join(hxs.select('*/div/text()').extract(), "")
            hxs = HtmlXPathSelector(text = webItem[6])
            object['weight']            = string.join(hxs.select('*/div/text()').extract(), "")
            hxs = HtmlXPathSelector(text = webItem[8])
            object['price']             = string.join(hxs.select('*/div/text()').extract(), "")
            hxs = HtmlXPathSelector(text = webItem[9])
            object['provider']          = string.join(hxs.select('*/div/text()').extract(), "")
            hxs = HtmlXPathSelector(text = webItem[10])
            object['producer']          = string.join(hxs.select('*/div/text()').extract(), "")
            objects.append(object)
        return objects

    def parse_start_url(self, response):
        return self.parse_base(response)

    def parse_item(self, response):
        return self.parse_base(response)