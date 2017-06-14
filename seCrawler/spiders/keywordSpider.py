from __future__ import unicode_literals

from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest

from seCrawler.common.searResultPages import SearResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors


class KeywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = ['google.com']
    keyword = None
    search_engine = None
    selector = None

    def __init__(self, keyword, se='google', pages=1,  *args, **kwargs):
        super(KeywordSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        self.keyword = keyword.lower()
        self.search_engine = se.lower()
        self.selector = SearchEngineResultSelectors[self.search_engine]
        page_urls = SearResultPages(keyword, se, int(pages))
        for url in page_urls:
            print(url)
            self.start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse)

    def parse(self, response):
        results = {
            'search_results': []
        }

        for se in Selector(response).xpath(self.selector['search_result_main_block']):
            url_title_block = se.xpath(self.selector['url_title_block'])
            url = url_title_block.xpath(self.selector['url']).extract_first()
            title = url_title_block.xpath(self.selector['title']).extract_first()
            description = ''.join(se.xpath(self.selector['description']).extract())

            results['search_results'].append({
                'url': url,
                'title': title,
                'description': description
            })

        images = Selector(response).xpath(self.selector['images']).extract()
        if images:
            results['images'] = images
        else:
            results['images'] = []

        return results
