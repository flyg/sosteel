# -*- coding=UTF-8 -*-
from scraper.items import SteelItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import string

class BaostarSpider(CrawlSpider):
    name = "baostar"
    allowed_domains = ["sss.baostar.com"]
    start_urls = ["http://sss.baostar.com/ss/search80.html"]

    def parse_base(self, response):
        modified_headers = response.request.headers
        modified_headers['Accept'] = 'text/html, */*; q=0.01'
        modified_headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        modified_headers['X-Requested-With'] = 'XMLHttpRequest'
        modified_headers['Referer'] = 'http://sss.baostar.com/ss/search80.html'
        modified_headers['Host'] = 'sss.baostar.com'
        modified_headers['Content-Length'] = '511'
        modified_headers['DNT'] = '1'
        modified_headers['Connection'] = 'Keep-Alive'
        modified_headers['Pragma'] = 'no-cache'

        return [Request(url="http://sss.baostar.com/ss/search80.html",
            method='POST',
            cookies={'stopflag':'false', 'flag':'true'},
            headers=modified_headers,
            body='inqu_status-0-segNo=00100&inqu_status-0-platRegion=80&inqu_status-0-ifNew=1&inqu_status-0-ifJP=1&inqu_status-0-ifNormal=1&limit=1000&offset=0&isAjax=true', #limit cannot go beyond 1000
            callback=self.parse_content)]

    def parse_content(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed")
            return
        hxs = HtmlXPathSelector(response)
        webItems = hxs.select('//*//tr[@class="odd"]') + hxs.select('//*//tr[@class="even"]')
        objects = [];
        for webItem in webItems:
            object = SteelItem()
            object['model']             = string.join(webItem.select('./td[1]/a/text()').extract(), "")
            object['url']               = "http://sss.baostar.com" + string.join(webItem.select('./td[1]/a/@href').extract(), "")
            object['trademark']         = string.join(webItem.select('./td[2]/text()').extract(), "")
            object['spec']              = string.join(webItem.select('./td[3]/text()').extract(), "")
            object['producer']          = "宁钢"
            object['origin']            = "宁波"
            #object['stock_location']    = string.join(webItem.select('./td[6]/text()').extract(), "")
            object['price']             = string.join(webItem.select('./td[5]/span/text()').re(r'\s*\t*(.*)\r\n'), "")
            object['weight']            = string.join(webItem.select('./td[4]/text()').extract(), "")
            #object['provider']          = string.join(webItem.select('./td[9]/div/a/text()').extract(), "")
            objects.append(object)
        return objects

    def parse_start_url(self, response):
        return self.parse_base(response)

    def parse_item(self, response):
        return self.parse_base(response)