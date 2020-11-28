import os
from scrapy import cmdline

# cmdline.execute("scrapy crawl scrapyDemo".split())


# 获取当前文件路径
dirpath = os.path.dirname(os.path.abspath(__file__))
dirpath = os.path.join(dirpath, "scrapyDemo")
print(dirpath)
# 切换到scrapy项目路径下
os.chdir(dirpath[:dirpath.rindex("\\")])
# 启动爬虫,第三个参数为爬虫name
cmdline.execute(['scrapy', 'crawl', 'FoxNewSpider'])
