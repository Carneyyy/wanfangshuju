# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class WfDataSpider(CrawlSpider):
    name = 'wf_data'
    allowed_domains = ['wanfangdata.com.cn']
    start_urls = ['http://www.wanfangdata.com.cn/index.html']

    rules = (
        Rule(LinkExtractor(
            allow=r'.*?/toIndex.do',
            restrict_xpaths='//div[@id="D1fBtb"]/div/a'
        ),
            callback='get_page_data',
            follow=True
        ),
    )
    def get_page_data(self,response):
        print(response.url,'==================================')
    #     http://www.wanfangdata.com.cn/search/searchList.do?
    #     searchType=legislations&
    #     showType=detail&
    #     pageSize=20&
    #     searchWord=法律
    # http://www.wanfangdata.com.cn/search/searchList.do?
    # searchType=legislations&
    # showType=&
    # pageSize=20
    # &searchWord=政治
    # &isTriggerTag=
    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
