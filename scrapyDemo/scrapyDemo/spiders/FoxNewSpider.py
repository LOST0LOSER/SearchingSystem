# -*- coding: utf-8 -*-
import scrapy
# from lxml import etree
# from bs4 import BeautifulSoup
# import requests
import os
import re
from scrapyDemo.items import newsItem
# from selenium import webdriver
# import json
# import requests
mainpath = os.path.dirname(os.getcwd())
Reuterspath = os.path.join(mainpath, "Reuters")
# print(mainpath)


class FoxNewSpider(scrapy.Spider):
    name = 'FoxNewSpider'
    host = "https://www.foxnews.com"
    allowed_domains = ['https://www.foxnews.com/']
    start_urls = [
                  "https://www.foxnews.com/",
                  "https://www.foxnews.com/category/us/crime",
                  "https://www.foxnews.com/category/us/military",
                  "https://www.foxnews.com/category/tech/topics/security",
                  "https://www.foxnews.com/category/tech/topics/computers",
                  "https://www.foxnews.com/category/science/air-and-space",
                  "https://www.foxnews.com/category/world/global-economy",
                  "https://www.foxbusiness.com/markets",
                  "https://www.foxnews.com/category/politics/house-of-representatives",
                  "https://www.foxnews.com/category/politics/executive",
                  "https://www.foxnews.com/category/world/conflicts",
                  "https://www.foxnews.com/food-drink",
                  "https://www.foxnews.com/auto",
                  "https://www.foxnews.com/category/faith-values/faith"
                ]

    # content_urls = []

    # driver = webdriver.PhantomJS()
    # client = webdriver.Chrome()
    # client = webdriver.Chrome()
    # def start_requests(self):
    # def getFoxnewInfo(self,word):
    #     url = self.start_urls[0]

    # list = []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)     

    def parse(self, response):
        # main crawler
        titles = response.xpath(
            '//main[@class="main-content"]//article')

        new_url = None
        content_urls = []
        for title in titles:
            new_url = title.xpath('.//a/@href').get().strip()
            if new_url is not None:
                if not re.match("https://", new_url):
                    new_url = self.host + new_url
                if new_url not in content_urls:
                    novideo = new_url[:20]
                    if novideo is not None and re.search("video", novideo) is None:
                        content_urls.append(new_url)
        for href in content_urls:
            yield scrapy.Request(url=href, callback=self.new_prase, dont_filter=True)

        # # 动态增加爬取目录的条目，动态页面解析
        # category = None
        # if "category" in response.url:
        #     category = response.url.split("/category/")[-1]

        #     moreurl = "https://www.foxnews.com/api/article-search"
        #     headers = {
        #         'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
        #         'referer': response.url
        #         # 'cookie': "user_trace_token=20170502200739-07d687303c1e44fa9c7f0259097266d6;"
        #     }
        #     searchparams = {
        #         "isCategory": False,
        #         "isTag": True,
        #         "isKeyword": False,
        #         "isFixed": False,
        #         "isFeedUrl": False,
        #         "searchSelected": "fox-news/"+category,
        #         "contentTypes": {
        #             "interactive": True,
        #             "slideshow": True,
        #             "video": False,
        #             "article": True,
        #             "size": 30,
        #             "offset": 1
        #         }
        #     }
        #     searchparams = json.dumps(searchparams)
        #     # size 个条目，其中不要视频
        #     # offset = 10
        #     for i in range(0, 2):
        #         # new_searchparams = "".join(
        #         #     ["&size=20&offset=", str(offset)])
        #         # new_searchparams = searchparams+new_searchparams
        #         # offset += 20
        #         res = requests.get(
        #             moreurl, headers=headers, params=searchparams)
        #         res_json = json.loads(res.text)

        #         for item in res_json:
        #             url = item["url"]
        #             if re.search("https://", url) is None:
        #                 url = self.host+url
        #                 if url not in self.content_urls:
        #                     self.content_urls.append(url)


    def new_prase(self, response):
        contentSelectorList = response.xpath(
            '//article[@class="article-wrap has-video"]')

        for contentSelector in contentSelectorList:
            title = contentSelector.xpath(
                './/h1[@class="headline"]/text()').extract()
            title = "".join(title)
            content = contentSelector.xpath(
                './/div[@class="article-content"]//p')
            content = content.xpath('string(.)').extract()
            content = " ".join(content)
            content = re.split("\xa0", content)
            content = " ".join(content).strip()
            yield {
                "title": title,
                "content": content
            }
