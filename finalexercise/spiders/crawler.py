# -*- coding: utf-8 -*-

import logging   # for logging
from logging.handlers import TimedRotatingFileHandler   # for logging

import scrapy
from scrapy.loader import ItemLoader   # for item loader

from finalexercise.items import FinalexerciseItem   # to load items for iteam loader

# log file setting
REGULAR_LOG_FILE = "FinalCrawler-log.log"   # all logs will be saved to this file
crawler_logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: [%(name)-12s] %(message)s')
# crawler_logger.setLevel(logging.DEBUG)

parse_fh = TimedRotatingFileHandler(
                                    # handler for all logs, and rotated at midnight and keep upto backup logs of the past 7 days
                                    REGULAR_LOG_FILE,
                                    when='midnight',
                                    interval=1,
                                    backupCount=7
                                )

parse_fh.setFormatter(formatter)   # setting the format for file handler
parse_fh.setLevel(logging.DEBUG)   # setting the level for each handler
crawler_logger.addHandler(parse_fh)   # adding the handlers


class FinalCrawler(scrapy.Spider):
    name = "final"

    def start_requests(self):
        urls = [
            'http://news.donga.com/List?ymd=20180423&m=NP',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        url_list = response.xpath(
            '//div[@id="contents"]/div[@class="articleList"]/div[@class="rightList"]/a/@href'
        ).extract()

        donga_urls = [u.encode('utf-8') for u in url_list]
        for each_article in donga_urls:
            # send each article url to parse_contents to parse contents of the article
            yield scrapy.Request(url=each_article, callback=self.parse_contents)


    def parse_contents(self, response):
        page = response.url
        crawler_logger.info("The url of the target is: {}".format(page))   # logging example

        item_loader = ItemLoader(item=FinalexerciseItem(), response=response)
        item_loader.add_xpath('author', '//div[@class="article_title"]/div[@class="title_foot"]/span[@class="report"]/a/text()')
        item_loader.add_value(
            'date',
            str(
                response.xpath(
                    '//div[@class="article_title"]/div[@class="title_foot"]/span[@class="date01"]/text()'
                ).extract()[-1].split(" ")[-2]
            )
        )
        item_loader.add_xpath('title', '//div[@class="article_title"]/h2[@class="title"]/text()')
        item_loader.add_value('url', response.url)

        return item_loader.load_item()