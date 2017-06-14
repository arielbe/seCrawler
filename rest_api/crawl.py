from json import dumps

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import defer

from seCrawler.spiders.keywordSpider import KeywordSpider


class Worker(object):
    def __init__(self):
        self._reset_items()
        self.runner = CrawlerRunner(get_project_settings())

    @defer.inlineCallbacks
    def run(self, keyword, pages):
        d = self.runner.crawl(KeywordSpider, keyword=keyword, pages=pages)
        for crawler in self.runner.crawlers:
            crawler.signals.connect(self._item_scraped, signal=signals.item_scraped)
        yield d

    def finish(self, finish, request):
        json_items = dumps(self.items)
        request.responseHeaders.addRawHeader('content-type', 'application/json')
        request.write(json_items)
        request.finish()
        self._reset_items()

    def _item_scraped(self, item, response, spider):
        search_results = self.items['search_results']
        for search_result in item['search_results']:
            search_results.append(search_result)

        images = self.items['images']
        for image in item['images']:
            images.append(image)

    def _reset_items(self):
        self.items = {
            'search_results': [],
            'images': []
        }
