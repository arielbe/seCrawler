from scrapy.selector import Selector
from scrapy.spiders import Spider

from seCrawler.common.searResultPages import SearResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors


class KeywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = ['bing.com', 'google.com', 'baidu.com']
    start_urls = []
    keyword = None
    search_engine = None
    selector = None

    def __init__(self, keyword, se='google.com', pages=1,  *args, **kwargs):
        super(KeywordSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword.lower()
        self.search_engine = se.lower()
        self.selector = SearchEngineResultSelectors[self.search_engine]
        page_urls = SearResultPages(keyword, se, int(pages))
        for url in page_urls:
            print(url)
            self.start_urls.append(url)

    def parse(self, response):
        for url in Selector(response).xpath(self.selector).extract():
            yield {'url': url}

        pass
