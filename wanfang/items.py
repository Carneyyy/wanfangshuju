# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WanfangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 中文标题
    title = scrapy.Field()
    # 英文标题
    English_title = scrapy.Field()
    # 摘要
    abstract =scrapy.Field()
    # doi
    dio =scrapy.Field()
    # 中文关键语
    keyword =scrapy.Field()
    # 英文关键词
    English_keyword =scrapy.Field()
    # 作者中文名
    auth =scrapy.Field()
    # 作者英文名
    auther =scrapy.Field()
    # 作者单位
    author_unit =scrapy.Field()
    # 刊名
    journal_name =scrapy.Field()
    # Journal
    Journal =scrapy.Field()
    # 年，卷（期）
    year_roll =scrapy.Field()
    # 所属期刊栏目
    category = scrapy.Field()
    # 分类号
    type_nums = scrapy.Field()
    # 基金项目
    jijin =scrapy.Field()
    # 出版日期
    publication_date =scrapy.Field()
    # 页数
    page_nums =scrapy.Field()
    # 页码
    page_m=scrapy.Field()

    """
    create table qikan ( id int auto_increment, 
                         title varchar(256),
                         English_title varchar(256),
                         abstract text,
                         dio varchar(128),
                         keyword varchar(128),
                         English_keyword varchar(128),
                         auth varchar(128),
                         auther varchar(128),
                         author_unit varchar(128),
                         journal_name varchar(128),
                         Journal varchar(128),
                         year_roll varchar(128),
                         category varchar(128),
                         type_nums varchar(128),
                         jijin varchar(128),
                         publication_date varchar(128),
                         page_nums varchar(128),
                         page_m varchar(128),
                         primary key(id));
    
    """
    def get_sql_str(self,item_dict):
        sql = """
                  INSERT INTO qikan (%s)
                  VALUES (%s)
                  """ % (
            ','.join(item_dict.keys()),
            ','.join(['%s'] * len(item_dict))
        )

        return sql

class WanFangXueWeiItem(scrapy.Item):

    # 中文标题
    title = scrapy.Field()
    # 中文关键词
    keyword = scrapy.Field()
    # 中文作者名
    auth = scrapy.Field()
    # 学位授权单位
    unit = scrapy.Field()
    # 授予学位
    degree = scrapy.Field()
    # 学科专业
    specialty = scrapy.Field()
    # 导师姓名
    tutor_name = scrapy.Field()
    # 学位年度
    degrees = scrapy.Field()
    # 语种
    language = scrapy.Field()
    # 分类号
    category = scrapy.Field()
    # 在线出版日期
    publication_date = scrapy.Field()
    """
    create table xuewei ( id int auto_increment,
                          title varchar(256),
                          keyword varchar(256),
                          auth varchar(256),
                          unit varchar(256),
                          degree varchar(256),
                          specialty varchar(256),
                          tutor_name varchar(256),
                          degrees varchar(256),
                          language varchar(256),
                          category varchar(256),
                          publication_date varchar(256),
                          primary key(id));
    
    
    """

    def get_sql_str(self, item_dict):
        sql = """
                     INSERT INTO xuewei (%s)
                     VALUES (%s)
                     """ % (
            ','.join(item_dict.keys()),
            ','.join(['%s'] * len(item_dict))
        )

        return sql

class WanFangZhuanLiItem(scrapy.Item):
    # 中文名称
    title = scrapy.Field()
    # 摘要
    abstract = scrapy.Field()
    # 专利类型
    patent_type = scrapy.Field()
    # 申请/专利号
    patent_nums = scrapy.Field()
    # 申请日期
    application_data = scrapy.Field()
    # 公开/公告号
    public = scrapy.Field()
    # 主分类号
    main_classnums = scrapy.Field()
    # 申请/专利权人
    patentee = scrapy.Field()
    # 发明/设计人
    designer = scrapy.Field()
    # 主申请人地址
    Address = scrapy.Field()
    # 专利代理机构
    patent_agency = scrapy.Field()
    # 代理人
    agent = scrapy.Field()
    # 国别省市代码
    Country_code = scrapy.Field()
    # 法律状态
    legal_status = scrapy.Field()

    """
    create table zhuanli(id int auto_increment,
                        title varchar(256),
                        abstract text,
                        patent_type varchar(256),
                        patent_nums varchar(256),
                        application_data varchar(256),
                        public varchar(256),
                        main_classnums varchar(256),
                        patentee varchar(256),
                        designer varchar(256),
                        Address varchar(256),
                        patent_agency varchar(256),
                        agent varchar(256),
                        Country_code varchar(256),
                        legal_status varchar(256),
                        primary key(id)):
    
    """
    def get_sql_str(self, item_dict):
        sql = """
                     INSERT INTO zhuanli (%s)
                     VALUES (%s)
                     """ % (
            ','.join(item_dict.keys()),
            ','.join(['%s'] * len(item_dict))
        )

        return sql

class WanFangHuiYiItem(scrapy.Item):
    # 中文标题
    title = scrapy.Field()
    # 摘要
    abstract = scrapy.Field()
    # 关键词
    keyword = scrapy.Field()
    # 作者
    auth = scrapy.Field()
    # 作者单位
    unit = scrapy.Field()
    # 母体文献
    literature = scrapy.Field()
    # 会议名称
    Cnference_Title = scrapy.Field()
    # 会议时间
    MeetingTime = scrapy.Field()
    # 会议地点
    meeting_place = scrapy.Field()
    # 主办单位
    MaiUnit = scrapy.Field()
    # 语种
    language = scrapy.Field()
    # 分类号
    class_nums = scrapy.Field()
    # 在线出版日期
    publication_date = scrapy.Field()
    # 页码
    pagination = scrapy.Field()
    """
    create table huiyi (id int auto_increment,
                        title varchar(256),
                        abstract text,
                        keyword varchar(256),
                        auth varchar(256),
                        unit varchar(256),
                        literature varchar(256),
                        Cnference_Title varchar(256),
                        MeetingTime varchar(256),
                        meeting_place varchar(256),
                        MaiUnit varchar(256),
                        language varchar(256),
                        class_nums varchar(256),
                        publication_date varchar(256),                        
                        pagination varchar(256),
                        primary key(id));
    """
    def get_sql_str(self, item_dict):
        sql = """
                     INSERT INTO huiyi (%s)
                     VALUES (%s)
                     """ % (
            ','.join(item_dict.keys()),
            ','.join(['%s'] * len(item_dict))
        )

        return sql

class WanFangFaGuiItem(scrapy.Item):
    # 中文标题
    title = scrapy.Field()
    # 库别名称
    KubeName = scrapy.Field()
    # 颁布部门
    Issued_department = scrapy.Field()
    # 效力级别
    Level_effectiveness = scrapy.Field()
    # 时效性
    failure = scrapy.Field()
    # 颁布日期
    issuance_date = scrapy.Field()
    # 实施日期
    material_date = scrapy.Field()
    # 内容分类
    content_class = scrapy.Field()
    """
    create table fagui (id int auto_increment,
                        title varchar(256),
                        KubeName varchar(256),
                        Issued_department varchar(256),
                        Level_effectiveness varchar(256),
                        failure varchar(256),
                        issuance_date varchar(256),
                        material_date varchar(256),
                        content_class varchar(256),
                        primary key(id));
    """
    def get_sql_str(self, item_dict):
        sql = """
                     INSERT INTO fagui (%s)
                     VALUES (%s)
                     """ % (
            ','.join(item_dict.keys()),
            ','.join(['%s'] * len(item_dict))
        )

        return sql

class WanFangKeJiBaoGaoItem(scrapy.Item):
    # 中文标题
    title = scrapy.Field()
    # 英文标题
    English_title = scrapy.Field()
    # 摘要
    abstract = scrapy.Field()
    # 中文关键语
    keyword = scrapy.Field()
    # 作者中文名
    auth = scrapy.Field()
    # 作者单位
    author_unit = scrapy.Field()
    # 报告类型
    report_tale = scrapy.Field()
    # 公开范围
    open_scope = scrapy.Field()
    # 全文页数
    all_pagination = scrapy.Field()
    # 项目/课题名称 
    task_name = scrapy.Field()
    # 计划名称
    Project_name = scrapy.Field()
    # 编制时间
    Compile_time = scrapy.Field()
    # 立项批准年
    project_approval_year = scrapy.Field()
    # 馆藏号
    Collection = scrapy.Field()
    """
    create table keji ( id int auto_increment,
                        title varchar(256),
                        English_title varchar(256),
                        abstract text,
                        keyword varchar(256),
                        auth varchar(256),
                        author_unit varchar(256),
                        report_tale varchar(256),
                        open_scope varchar(256),
                        all_pagination varchar(256),
                        task_name varchar(256),
                        Project_name varchar(256),
                        Compile_time varchar(256),
                        project_approval_year varchar(256),
                        Collection varchar(256),
                        primary key(id));
    """

    def get_sql_str(self, item_dict):
        sql = """
                     INSERT INTO keji (%s)
                     VALUES (%s)
                     """ % (
            ','.join(item_dict.keys()),
            ','.join(['%s'] * len(item_dict))
        )

        return sql
