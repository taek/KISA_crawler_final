# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

from scrapy import signals   # For json export
from scrapy.exporters import JsonLinesItemExporter   # For json export
from scrapy.exporters import CsvItemExporter   # For CSV export

JSON_FILE_NAME = "crawled-final-values.jsonl"
CSV_FILE_NAME = "crawled-final-values.csv"

# class to export items to json
class FinalexerciseJsonExportPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        filename = JSON_FILE_NAME
        if os.path.exists(filename):
            write_mode = "a+b"   # append if the file already exists
        else:
            write_mode = "w+b"   # create a file and write to it if the file does not exist yet
        file = open(filename, write_mode)
        self.files[spider] = file
        self.exporter = JsonLinesItemExporter(file, ensure_ascii=False)   # "ensure_ascii=False" is NEEDED for Korean
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class FinalexerciseCSVExportPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        filename = CSV_FILE_NAME
        if os.path.exists(filename):
            write_mode = "a+b"   # append if the file already exists
        else:
            write_mode = "w+b"   # create a file and write to it if the file does not exist yet
        file = open(filename, write_mode)
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)   # "ensure_ascii=False" is NEEDED for Korean
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
