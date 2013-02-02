from scraper.items import SteelItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
import string

class UsteelSpider(CrawlSpider):
    name = "usteel"
    allowed_domains = ["shop.usteel.com"]
    start_urls = ["http://shop.usteel.com/index.php?app=gangcai", "http://shop.usteel.com/index.php?app=buxiu"]

    rules = (
        Rule(SgmlLinkExtractor(allow = (r'index.php\?app=gangcai&page=\d{1,2}\b', ), deny = ('id=', 'city=', 'material=', 'manufacturer=', 'morespec=', 'specification=', 'cate_name=', 'morecat=', 'surface=', 'moresur=', )), callback = 'parse_item', follow = True),
        Rule(SgmlLinkExtractor(allow = (r'index.php\?app=buxiu&page=\d{1,2}\b', ), deny = ('id=', 'city=', 'material=', 'manufacturer=', 'morespec=', 'specification=', 'cate_name=', 'morecat=', 'surface=', 'moresur=', )), callback = 'parse_item', follow = True),
    )

    def parse_base(self, response):
        hxs = HtmlXPathSelector(response)
        webItems = hxs.select('//*//div[@class="result mb10"]//ul[@class="list"]/li')
        objects = [];
        for webItem in webItems:
            object = SteelItem()
            object['model']             = string.join(webItem.select('*/span[@class="s1 textL"]/a/@title').extract(), "")
            object['url']               = "http://shop.usteel.com/" + string.join(webItem.select('*/span[@class="s1 textL"]/a/@href').extract(), "")
            object['trademark']         = string.join(webItem.select('*/span[@class="s2"]/text()').extract(), "")
            object['spec']              = string.join(webItem.select('*/span[@class="s3"]/text()').extract(), "")
            object['producer']          = string.join(webItem.select('*/span[@class="s4"]/text()').extract(), "")
            object['origin']            = string.join(webItem.select('*/span[@class="s5"]/text()').extract(), "") + string.join(webItem.select('*/span[@class="s5"]/i/text()').extract(), "")
            object['price']             = string.join(webItem.select('*/span[@class="s6"]/b/text()').extract(), "")
            object['weight']            = string.join(webItem.select('*/span[@class="s6"]/i[2]/text()').extract(), "")
            object['provider']          = string.join(webItem.select('*/span[@class="s8 textL"]/a/@title').extract(), "")
            objects.append(object)
        return objects

    def parse_start_url(self, response):
        return self.parse_base(response)

    def parse_item(self, response):
        return self.parse_base(response)