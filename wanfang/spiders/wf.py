# -*- coding: utf-8 -*-
import scrapy
from wanfang.items import WanfangItem,WanFangXueWeiItem,WanFangFaGuiItem,WanFangHuiYiItem,WanFangKeJiBaoGaoItem,WanFangZhuanLiItem
import re,requests
from lxml.html import etree
class WfSpider(scrapy.Spider):
    name = 'wf'
    allowed_domains = ['wanfangdata.com.cn']
    # http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id=jhxk201703024
    # http://d.old.wanfangdata.com.cn/Periodical/jhxk201703024
    # http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_QK&f=top
    # http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_XW&f=top
    # http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_HY&f=top
    # http://s.wanfangdata.com.cn/NSTR.aspx?q=%E6%B3%95%E5%BE%8B&f=top
    # http://s.wanfangdata.com.cn/Claw.aspx?q=%E6%B3%95%E5%BE%8B&f=top
    # http://www.wanfangdata.com.cn/search/searchList.do?searchType=tech&showType=detail&pageSize=20&searchWord=%E6%B3%95%E5%BE%8B&isTriggerTag=
    # http://www.wanfangdata.com.cn/search/searchList.do?searchType=legislations&showType=detail&pageSize=20&searchWord=%E6%B3%95%E5%BE%8B&isTriggerTag=
    # http://www.wanfangdata.com.cn/search/searchList.do?searchType=legislations&showType=&pageSize=20&searchWord=%E6%94%BF%E6%B2%BB&isTriggerTag=
    url = [
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=patent&showType=&pageSize=&searchWord=法律&isTriggerTag='
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=tech&showType=detail&pageSize=20&searchWord=法律&isTriggerTag='
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=perio&showType=detail&pageSize=20&searchWord=法律&isTriggerTag='
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=conference&showType=detail&pageSize=20&searchWord=法律&isTriggerTag='
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=degree&showType=detail&pageSize=20&searchWord=法律&isTriggerTag='
        'http://www.wanfangdata.com.cn/search/searchList.do?searchType=legislations&showType=&pageSize=20&searchWord=法律&isTriggerTag='
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=conference&showType=detail&pageSize=20&searchWord=政治&isTriggerTag='
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=legislations&showType=detail&pageSize=20&searchWord=政治&isTriggerTag='
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=tech&showType=detail&pageSize=20&searchWord=政治&isTriggerTag='
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=perio&showType=detail&pageSize=20&searchWord=政治&isTriggerTag='
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=degree&showType=detail&pageSize=20&searchWord=政治&isTriggerTag='
        # 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=patent&showType=&pageSize=&searchWord=政治&isTriggerTag='
    ]
    start_urls = url
    def parse(self, response):
        callback = None
        pattern = re.compile('.*?searchType=(.*?)&',re.S)
        get_parse = re.findall(pattern,response.url)[0]
        # print(get_parse)
        if get_parse == 'tech':
            callback = self.get_old_tech_data
        elif get_parse == 'perio':
            callback = self.get_old_perio_data_
        elif get_parse == 'conference':
            callback = self.get_old_conference_data
        elif get_parse == 'degree':
            callback = self.get_old_degree_data
        elif get_parse == 'legislations':
            callback = self.get_old_legislations_data
        elif get_parse == 'patent':
            callback = self.get_old_patent_data
        yield scrapy.Request(
            url=response.url,
            callback=callback
        )

    # 期刊详情解析
    def get_perio_data(self,response):

        item = WanfangItem()
        print(response.url,'=========================')
        # 中文标题
        item['title'] = response.xpath('//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first().replace(' ','').replace('\r','').replace('\n','').replace('\t','')
        # 英文标题
        item['English_title'] = response.xpath('//div[@class="left_con_top"]/div[@class="English"]/text()').extract_first('暂无').replace(' ','').replace('\r','').replace('\n','').replace('\t','')
        # 摘要
        item['abstract'] = response.xpath('//div[@id="see_alldiv"]/text()').extract_first('暂无').replace(' ','').replace('\r','').replace('\n','').replace('\t','').replace('\xa0\xa0','')
        detail = response.xpath('//ul[@class="info"]')
        # for detail in details:
        # doi
        if detail.xpath('./li[1]/div[@class="info_left"]/text()').extract_first('') == "doi：":
            item['dio'] = detail.xpath('.//a/text()').extract_first('').replace('\t', '').replace(' ', '')
        elif detail.xpath('./li[2]/div[@class="info_left"]/text()').extract_first('') == "关键词：":
            #关键词
            item['keyword'] = '、'.join(detail.xpath('.//a/text()').extract())
        elif detail.xpath('./li[3]/div[@class="info_left"]/text()').extract_first('') == "Keyword：":
            # 英文关键词
            item['English_keyword'] = '、'.join(detail.xpath('.//a/text()').extract())
        elif detail.xpath('./li[4]/div[@class="info_left"]/text()').extract_first('') == "作者：":
            # 作者
            item['auth'] = '、'.join(detail.xpath('./div[2]/a/text()').extract())
        elif detail.xpath('./li[5]/div[@class="info_left"]/text()').extract_first('') == "Author：":
            # 作者英文名
            item['auther'] = '、'.join(detail.xpath('.//a/text()').extract()).replace('\n', '')
        elif detail.xpath('./li[6]/div[@class="info_left"]/text()').extract_first('') == "作者单位：":
            # 作者单位
            item['author_unit'] = '、'.join(detail.xpath('.//a/text()').extract())
        elif detail.xpath('./li[7]/div[@class="info_left"]/text()').extract_first('') == "刊名：":
            # 刊名
            item['journal_name'] = detail.xpath('.//a[@class="college"]/text()').extract_first('')
        elif detail.xpath('./li[8]/div[@class="info_left"]/text()').extract_first('') == "Journal：":
            # Journal
            item['Journal'] = detail.xpath('.//a[1]/text()').extract_first('')
            if len(item['Journal']) == 0:
                item['Journal'] = detail.xpath('.///text()').extract_first('').replace('\r\n', '').replace(' ','').replace('\t', '')
        elif detail.xpath('./li[9]/div[@class="info_left"]/text()').extract_first('') == "年，卷(期)：":
            # 年，卷(期)
            item['year_roll'] = detail.xpath('.//a/text()').extract_first('')
            if len(item['year_roll']) == 0:
                item['year_roll'] = detail.xpath('.//text()').extract_first('').replace('\r\n', '').replace(' ','').replace('\t', '')
        elif detail.xpath('./li[10]/div[@class="info_left"]/text()').extract_first('') == "所属期刊栏目：":
            # 所属期刊栏目
            item['category'] = detail.xpath('.//a/text()').extract_first('')
            if len(item['category']) == 0:
                item['category'] = detail.xpath('.//a/text()').extract_first('').replace('\r\n', '').replace(' ','').replace('\t', '')
        elif detail.xpath('./li[11]/div[@class="info_left"]/text()').extract_first('') == "分类号：":
            # 分类号
            item['type_nums'] = detail.xpath('.//div[2]/text()').extract_first('').replace('\r', '').replace('\n','').replace('\t', '')
        elif detail.xpath('./li[12]/div[@class="info_left"]/text()').extract_first('') == "基金项目：":
            # 基金项目
            item['jijin'] = detail.xpath('.//a[1]/text()').extract_first('')
        elif detail.xpath('./li[13]/div[@class="info_left"]/text()').extract_first('') == "在线出版日期：":
            # 在线出版日期
            item['publication_date'] = detail.xpath('.//text()').extract_first('').replace('\r\n', '').replace(' ','').replace('\t', '')
        elif detail.xpath('./li[14]/div[@class="info_left"]/text()').extract_first('') == "页数：":
            # 页数
            item['page_nums'] = detail.xpath('.//text()').extract_first('').replace(' ', '')
        elif detail.xpath('./li[15]/div[@class="info_left"]/text()').extract_first('') == "页码：":
            # 页码
            item['page_m'] = detail.xpath('.//text()').extract_first('').replace(' ', '')
        # yield item
        print(item)
        # 期刊列表解析
    # 期刊列表解析
    def get_old_perio_data_(self, response):
        ids = []
        send_url = [
            'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%94%BF%E6%B2%BB%20DBID%3AWF_QK&f=top'
            # 'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_QK&f=top'
            # ?q=%e6%b3%95%e5%be%8b+DBID%3aWF_QK&f=top&p=2
            ]
        for i in send_url:
            detail_url = requests.get(url=i)
            detail_page = detail_url.text
            detail_html = etree.HTML(detail_page)
            details = detail_html.xpath('//div[@class="record-item-list"]/div[@class="record-item"]')
            for detail in details:
                old_detail_url = detail.xpath('.//div[@class="record-title"]/a[@class="title"]/@href')[0]+'/'
                print(old_detail_url)
                # http://d.old.wanfangdata.com.cn/Periodical/jhxk201703024
                pattern = re.compile('.*?Periodical/(.*?)/')
                n_ids = re.findall(pattern,old_detail_url)
                ids.append(n_ids)
                # print(ids,'======')
            # try:
                # next_url = detail_html.xpath('//div[@class="record-item-list"]/p[@class="pager"]/a[last()]/@href')[0]
                # print(next_url)
                # if next_url:
                #     url = 'http://s.wanfangdata.com.cn/Paper.aspx'+ next_url
                #     # http://s.wanfangdata.com.cn/Paper.aspx?q=%e6%b3%95%e5%be%8b&f=top&p=2
                #     send_url.append(url)
                #     self.get_old_perio_data_(response)
            for id in ids:
                yield scrapy.Request(
                    # http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id=jhxk201703024
                    url='http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id={}'.format(id[0]),
                    callback=self.get_perio_data,
                )
            # except Exception as err:
            #     if err == 'list index out of range':
            #         print('期刊分类数据加载完毕')

    # 学位列表解析
    def get_old_degree_data(self,response):
        ids = None
        send_url = [
            # 'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_XW&f=top'
            'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%94%BF%E6%B2%BB%20DBID%3AWF_XW&f=top'
        ]
        for url in send_url:
            old_html = requests.get(url=url)
            detail_page = old_html.text
            detail_html = etree.HTML(detail_page)
            details = detail_html.xpath('//div[@class="record-item-list"]/div[@class="record-item"]')
            for detail in details:
                old_detail_url = detail.xpath('.//div[@class="record-title"]/a[@class="title"]/@href')[0] + '/'
                print(old_detail_url)
                # http://d.old.wanfangdata.com.cn/Thesis/D492340/
                pattern = re.compile('.*?Thesis/(.*?)/')
                ids = re.findall(pattern, old_detail_url)
                print(ids,'======')
                try:
                    next_url = detail_html.xpath('//div[@class="record-item-list"]/p[@class="pager"]/a[last()]/@href')[0]
                    print(next_url)
                    if next_url:
                        n_url = 'http://s.wanfangdata.com.cn/Paper.aspx'+ next_url
                        # http://s.wanfangdata.com.cn/Paper.aspx?q=%e6%b3%95%e5%be%8b+DBID%3aWF_XW&f=top&p=2
                        send_url.append(n_url)
                        print(n_url)
                        self.get_old_degree_data(response)
                    for id in ids:
                        yield scrapy.Request(
                            # http://www.wanfangdata.com.cn/details/detail.do?_type=degree&id=D01706879
                            url='http://www.wanfangdata.com.cn/details/detail.do?_type=degree&id={}'.format(id),
                            callback=self.get_degree_data,
                        )
                except Exception as err:
                    if err == 'list index out of range':
                        print('学位分类数据加载完毕')

    # 学位详情解析
    def get_degree_data(self,response):
        item = WanFangXueWeiItem()
        print(response.url)
        """
        title = scrapy.Field()
         = scrapy.Field()
         = scrapy.Field()
         = scrapy.Field()
         = scrapy.Field()
         = scrapy.Field()
         = scrapy.Field()
         = scrapy.Field()
         = scrapy.Field()
         = scrapy.Field()
         = scrapy.Field()
        see_alldiv
        
                        
                                             

        """
        # 中文标题
        item['title'] = response.xpath('//div[@class="left_con_top"]/div[@class="title"]/text()').extract()[1].replace(' ','').replace('\r','').replace('\n','').replace('\t','')
        details = response.xpath('//ul[@class="info"]/li')
        for detail in details:
            # 中文关键词
            if detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '关键词：':
                item['keyword'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '作者：':
                # 中文作者名
                item['auth'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '学位授予单位：':
                # 学位授予单位
                item['unit'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '授予学位：':
                # 授予学位
                item['degree'] = '、'.join(detail.xpath('./div[2]/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '学科专业：':
                # 学科专业
                item['specialty'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '导师姓名：':
                # 导师姓名
                item['tutor_name'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '学位年度：':
                # 学位年度
                item['degrees'] = '、'.join(detail.xpath('./div[2]/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '语种：':
                # 语种
                item['language'] = detail.xpath('./div[2]/text()').extract_first().replace(' ','').replace('\r','').replace('\n','').replace('\t','')

            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '分类号：':
                # 分类号
                item['category'] = detail.xpath('./div[2]/text()').extract_first().replace(' ','').replace('\r','').replace('\n','').replace('\t','')

            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '在线出版日期：':
                # 在线出版日期
                item['publication_date'] = detail.xpath('./div[2]/text()').extract_first().replace(' ','').replace('\r','').replace('\n','').replace('\t','')



        yield item
        # print(item)
    # 会议列表解析
    def get_old_conference_data(self,response):
        ids = []
        send_url = [
            'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%94%BF%E6%B2%BB%20DBID%3AWF_HY&f=top'
            # 'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_HY&f=top'
            # ?q=%e6%b3%95%e5%be%8b+DBID%3aWF_QK&f=top&p=2
        ]
        for i in send_url:
            detail_url = requests.get(url=i)
            detail_page = detail_url.text
            detail_html = etree.HTML(detail_page)
            details = detail_html.xpath('//div[@class="record-item-list"]/div[@class="record-item"]')
            for detail in details:
                old_detail_url = detail.xpath('.//div[@class="record-title"]/a[@class="title"]/@href')[0] + '/'
                # print(old_detail_url)
                # http://d.old.wanfangdata.com.cn/Conference/7730508
                pattern = re.compile('.*?Conference/(.*?)/')
                d_id = re.findall(pattern, old_detail_url)
                ids.append(d_id)
            try:
                next_url = detail_html.xpath('//div[@class="record-item-list"]/p[@class="pager"]/a[last()]/@href')[0]
                print(next_url)
                if next_url:
                    url = 'http://s.wanfangdata.com.cn/Paper.aspx' + next_url
                    #http://s.wanfangdata.com.cn/Paper.aspx?q=%e6%b3%95%e5%be%8b+DBID%3aWF_HY&f=top&p=2
                    send_url.append(url)
                    self.get_old_conference_data(response)
                for id in ids:

                    yield scrapy.Request(
                        # http://www.wanfangdata.com.cn/details/detail.do?_type=conference&id=9516620
                        url='http://www.wanfangdata.com.cn/details/detail.do?_type=conference&id={}'.format(id[0]),
                        callback=self.get_conference_data,
                     )
            except Exception as err:
                if err == 'list index out of range':
                    print('会议分类数据加载完毕')

    # 会议详情解析
    def get_conference_data(self,response):
        item = WanFangHuiYiItem()
        print(response.url)
        # 中文标题
        item['title'] = response.xpath('//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first().replace(' ', '').replace('\r','').replace('\n', '').replace('\t', '')
        # 摘要
        item['abstract'] = response.xpath('//div[@id="see_alldiv"]/text()').extract_first('暂无').replace(' ','').replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0\xa0', '').replace('\u3000','')
        details = response.xpath('//ul[@class="info"]/li')
        for detail in details:
            # 关键词
            if detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '关键词：':
                item['keyword'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '作者：':
                # 作者
                item['auth'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '作者单位：':
                # 作者单位
                item['unit'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '母体文献：':
                # 母体文献
                item['literature'] = '、'.join(detail.xpath('./div[2]/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '会议名称：':
                # 会议名称
                item['Cnference_Title'] = detail.xpath('.//a/text()').extract()[1].replace('\r','').replace('\t','').replace('\n','')
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '会议时间：':
                # 会议时间
                item['MeetingTime'] = detail.xpath('./div[2]/text()').extract()[0].replace('\r','').replace('\t','').replace('\n','').replace(' ','')
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '会议地点：':
                # 会议地点
                item['meeting_place'] = '、'.join(detail.xpath('./div[2]/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '主办单位：':
                # 主办单位
                item['MaiUnit'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '语种：':
                # 语种
                item['language'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '分类号：':
                # 分类号
                item['class_nums'] = detail.xpath('./div[2]/text()').extract()[0].replace('\r','').replace('\t','').replace('\n','')
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '在线出版日期：':
                # 在线出版日期
                item['publication_date'] = detail.xpath('./div[2]/text()').extract()[0].replace('\r','').replace(' ','').replace('\n','').replace('\t','')
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == '页码：':
                # 页码
                item['pagination'] = '、'.join(detail.xpath('./div[2]/text()').extract())

        yield item
        # print(item)
    # 科技报告列表解析
    def get_old_tech_data(self,response):
        ids = []
        send_url = [
            # 'http://s.wanfangdata.com.cn/NSTR.aspx?q=%E6%B3%95%E5%BE%8B&f=top'
            'http://s.wanfangdata.com.cn/NSTR.aspx?q=%E6%94%BF%E6%B2%BB&f=top'
        ]
        for i in send_url:
            detail_url = requests.get(url=i)
            detail_page = detail_url.text
            detail_html = etree.HTML(detail_page)
            details = detail_html.xpath('//div[@class="record-item-list"]/div[@class="record-item"]')
            for detail in details:
                old_detail_url = detail.xpath('.//div[@class="record-title"]/a[@class="title"]/@href')[0] + '/'
                print(old_detail_url)
                #http://d.old.wanfangdata.com.cn/NSTR/66753/
                pattern = re.compile('.*?NSTR/(.*?)/')
                d_id = re.findall(pattern, old_detail_url)
                ids.append(d_id)
            try:
                next_url = detail_html.xpath('//div[@class="record-item-list"]/p[@class="pager"]/a[last()]/@href')[0]
                print(next_url)
                if next_url:
                    url = 'http://s.wanfangdata.com.cn/NSTR.aspx' + next_url
                    # http://s.wanfangdata.com.cn/NSTR.aspx?q=%e6%b3%95%e5%be%8b&f=top&p=2
                    send_url.append(url)
                    self.get_old_degree_data(response)
                for id in ids:

                    yield scrapy.Request(
                        # http://www.wanfangdata.com.cn/details/detail.do?_type=tech&id=66753
                        url='http://www.wanfangdata.com.cn/details/detail.do?_type=tech&id={}'.format(id[0]),
                        callback=self.get_tech_data,
                     )
            except Exception as err:
                if err == 'list index out of range':
                    print('科技报告分类数据加载完毕')

    # 科技报告详情解析
    def get_tech_data(self,response):
        item = WanFangKeJiBaoGaoItem()
        print(response.url)
        """
                科技报告
                       
                              
        """
        # 中文标题
        item['title'] = response.xpath('//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first().replace(' ', '').replace('\r','').replace('\n', '').replace('\t', '')
        # 英文标题
        item['English_title'] = response.xpath('//div[@class="left_con_top"]/div[@class="English"]/text()').extract_first('暂无').replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
        # 摘要
        item['abstract'] = response.xpath('//div[@id="see_alldiv"]/text()').extract_first('暂无').replace(' ','').replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0\xa0', '')
        details = response.xpath('//ul[@class="info"]/li')
        for detail in details:
            # 中文关键语
            if detail.xpath('./div[@class="info_left"]/text()').extract_first('') == "关键词：":
                item['keyword'] = '、'.join(detail.xpath('.//a/text()').extract())  #.replace('\t', '').replace(' ', '')
            elif detail.xpath('./div[@class="info_left "]/text()').extract_first('') == "作者：":
                # 作者中文名
                item['auth'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == "作者单位：":
                # 作者单位
                item['author_unit'] = '、'.join(detail.xpath('.//a/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == "报告类型：":
                # 报告类型
                item['report_tale'] = '、'.join(detail.xpath('./div[2]/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == "公开范围：":
                #公开范围
                item['open_scope'] = '、'.join(detail.xpath('./div[2]/text()').extract()).replace('\n', '')
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == "全文页数：":
                # 全文页数
                item['all_pagination'] = '、'.join(detail.xpath('./div[2]/text()').extract())
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == "项目/课题名称：":
                # 项目/课题名称 
                item['task_name'] = detail.xpath('.//a[@class="college"]/text()').extract_first('')
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == "计划名称：":
                # 计划名称
                item['Project_name'] = detail.xpath('./div[2]/text()').extract_first('')
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == "编制时间：":
                # 编制时间
                item['Compile_time'] = detail.xpath('./div[2]/text()').extract_first('').replace('\r','').replace('\t','').replace('\n','').replace(' ','')
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == "立项批准年：":
                # 立项批准年
                item['project_approval_year'] = detail.xpath('./div[2]/text()').extract_first('')
            elif detail.xpath('./div[@class="info_left"]/text()').extract_first('') == "馆藏号：":
                # 馆藏号
                item['Collection'] = detail.xpath('./div[2]/text()').extract_first('')
        yield item
        # print(item)
    # 法规列表解析
    def get_old_legislations_data(self,response):
        ids = []
        send_url = [
            # 'http://s.wanfangdata.com.cn/Claw.aspx?q=%E6%B3%95%E5%BE%8B&f=top'
            'http://s.wanfangdata.com.cn/Claw.aspx?q=%E6%94%BF%E6%B2%BB&f=top'
        ]
        for i in send_url:
            detail_url = requests.get(url=i)
            detail_page = detail_url.text
            detail_html = etree.HTML(detail_page)
            details = detail_html.xpath('//div[@class="record-item-list"]/div[@class="record-item"]')
            for detail in details:
                old_detail_url = detail.xpath('.//div[@class="record-title"]/a[@class="title"]/@href')[0] + '/'
                print(old_detail_url)
                # http://d.old.wanfangdata.com.cn/Claw/G000290411
                pattern = re.compile('.*?Claw/(.*?)/')
                d_id = re.findall(pattern, old_detail_url)
                ids.append(d_id)
            try:
                next_url = detail_html.xpath('//div[@class="record-item-list"]/p[@class="pager"]/a[last()]/@href')[0]
                print(next_url)
                if next_url:
                      # http://s.wanfangdata.com.cn/Claw.aspx?q=%e6%b3%95%e5%be%8b&f=top&p=2
                    url = 'http://s.wanfangdata.com.cn/Claw.aspx' + next_url
                    send_url.append(url)
                    self.get_old_legislations_data(response)
                for id in ids:
                    yield scrapy.Request(
                        # http://www.wanfangdata.com.cn/details/detail.do?_type=legislations&id=G000290937
                        url='http://www.wanfangdata.com.cn/details/detail.do?_type=legislations&id={}'.format(id[0]),
                        callback=self.get_legislations_data,
                    )
            except Exception as err:
                if err == 'list index out of range':
                    print('法规分类数据加载完毕')

    # 法规详情解析
    def get_legislations_data(self,response):
        item = WanFangFaGuiItem()
        print(response.url)
        # 中文标题
        item['title'] = response.xpath('//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('').replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        details = response.xpath('//ul[@class="info"]')
        # 库别名称
        item['KubeName'] = details.xpath('./li[1]/div[2]/text()').extract_first('').replace('\r','').replace('\n','').replace('\t','')
        # 颁布部门
        item['Issued_department'] = details.xpath('./li[3]/div[2]/text()').extract_first('').replace('\r','').replace('\n','').replace('\t','')
        # 效力级别
        item['Level_effectiveness'] = details.xpath('./li[4]/div[2]/text()').extract_first('').replace('\r','').replace('\n','').replace('\t','')
        # 时效性
        item['failure'] = details.xpath('./li[5]/div[2]/text()').extract_first('').replace('\r','').replace('\n','').replace('\t','')
        # 颁布日期
        item['issuance_date'] = details.xpath('./li[6]/div[2]/text()').extract_first('').replace('\r','').replace('\n','').replace('\t','')
        # 实施日期
        item['material_date'] = details.xpath('./li[7]/div[2]/text()').extract_first('').replace('\r','').replace('\n','').replace('\t','')
        # 内容分类
        item['content_class'] = details.xpath('./li[8]/div[2]/text()').extract_first('').replace('\r','').replace('\n','').replace('\t','')
        # yield item
        print(item)
    # 专利列表解析
    def get_old_patent_data(self,response):
        ids = []
        send_url = [
            # 'http://s.wanfangdata.com.cn/patent.aspx?q=%E6%B3%95%E5%BE%8B&f=top'
            'http://s.wanfangdata.com.cn/patent.aspx?q=%E6%94%BF%E6%B2%BB&f=top'
        ]
        for i in send_url:
            detail_url = requests.get(url=i)
            detail_page = detail_url.text
            detail_html = etree.HTML(detail_page)
            details = detail_html.xpath('//div[@class="record-item-list"]/div[@class="record-item"]')
            for detail in details:
                old_detail_url = detail.xpath('.//div[@class="record-title"]/a[@class="title"]/@href')[0] + '/'
                print(old_detail_url)
                # http://d.old.wanfangdata.com.cn/Patent/CN201710780234.6/
                pattern = re.compile('.*?Patent/(.*?)/')
                d_id = re.findall(pattern, old_detail_url)
                ids.append(d_id)
            try:
                next_url = detail_html.xpath('//div[@class="record-item-list"]/p[@class="pager"]/a[last()]/@href')[0]
                print(next_url)
                if next_url:
                    url = 'http://s.wanfangdata.com.cn/patent.aspx' + next_url
                    # http://s.wanfangdata.com.cn/patent.aspx?q=%e6%b3%95%e5%be%8b&f=top&p=2
                    send_url.append(url)
                    self.get_old_legislations_data(response)
                for id in ids:
                    yield scrapy.Request(
                        # http://www.wanfangdata.com.cn/details/detail.do?_type=patent&id=CN201711372221.1
                        url='http://www.wanfangdata.com.cn/details/detail.do?_type=patent&id={}'.format(id[0]),
                        callback=self.get_Patent_data,
                    )
            except Exception as err:
                if err == 'list index out of range':
                    print('专利分类数据加载完毕')

    # 专利详情解析
    def get_Patent_data(self,response):
        item = WanFangZhuanLiItem()
        print(response.url)
        """
        专利：
             
        """
        # 中文名称
        item['title'] = response.xpath('//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('').replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        # 摘要
        item['abstract'] = response.xpath('//div[@id="see_alldiv"]/text()').extract_first('暂无').replace(' ','').replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0\xa0', '')
        detail = response.xpath('//ul[@class="info"]')
        # for detail in details:
        # 专利类型
        item['patent_type'] = detail.xpath('./li[1]/div[2]/text()').extract_first('')
        # 申请/专利号
        item['patent_nums'] = detail.xpath('./li[2]/div[2]/text()').extract_first('')
        # 申请日期
        item['application_data'] = detail.xpath('./li[3]/div[2]/text()').extract_first('')
        # 公开/公告号
        item['public'] = detail.xpath('./li[4]/div[2]/text()').extract_first('')
        # 主分类号
        item['main_classnums'] = detail.xpath('./li[6]/div[2]/text()').extract_first().replace('\r','').replace('\n','').replace('\t','').replace('\xa0','')
        # 申请/专利权人 
        item['patentee'] = detail.xpath('./li[8]/div[2]/a/text()').extract_first().replace('\r','').replace('\n','').replace('\t','')
        # 发明/设计人
        item['designer'] = '、'.join(detail.xpath('./li[9]/div[2]/a/text()').extract())
        # 主申请人地址
        item['Address'] = detail.xpath('./li[10]/div[2]/text()').extract_first()
        # 专利代理机构
        item['patent_agency'] = detail.xpath('./li[11]/div[2]/text()').extract_first()
        # 代理人
        item['agent'] = detail.xpath('./li[12]/div[2]/text()').extract_first()
        # 国别省市代码
        item['Country_code'] = detail.xpath('./li[13]/div[2]/text()').extract_first()
        # 法律状态
        item['legal_status'] = detail.xpath('./li[last()]/div[2]/a/text()').extract_first()
        yield item
        # print(item)
