# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
# from scrapy import item
mainpath = os.path.dirname(os.getcwd())
Reuterspath = os.path.join(mainpath, "Reuters")


class ScrapydemoPipeline:
    def __init__(self):
        pass

    # def open_spider(self ,item ,spider):
    #     pass

    def process_item(self, item, spider):
        items = os.listdir(Reuterspath)
        newfileNumber = items.__len__()
        newfileNumber = str(newfileNumber)
        filename = "".join([newfileNumber, ".json"])
        filepath = os.path.join(Reuterspath, filename)
        item_json = json.dumps(item)
        file = open(filepath, "w+", encoding="utf8")
        file.writelines(item_json+"\n")
        file.close()

        return item

    def close_spider(self, spider):
        # self.file.close()
        pass
