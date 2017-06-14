from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.server import Site

from crawl import Worker


class CrawlerAPI:
    class RestInterface(object):

        def __init__(self):
            reactor.listenTCP(8888, self.create_site_tree())

        def create_site_tree(self):
            root = Resource()
            root.putChild('crawler', CrawlerAPI.RestInterface.ResultsPage())
            return Site(root)

        class ResultsPage(Resource):
            isLeaf = True

            def __init__(self):
                self.worker = Worker()
                Resource.__init__(self)

            def render_GET(self, request):
                args = request.args

                keyword = args.get('keyword')
                pages = args.get('pages')

                if not keyword or not pages:
                    return 'Missing arguments.'

                try:
                    pages = int(pages[0])
                except ValueError:
                    return 'Illegal pages number.'

                keyword = keyword[0]

                d = self.worker.run(keyword, pages)
                d.addCallback(self.worker.finish, request)

                return NOT_DONE_YET

    def __init__(self):
        self.interface = CrawlerAPI.RestInterface()

    def start(self):
        reactor.run()


def main():
    api = CrawlerAPI()
    api.start()

if __name__ == '__main__':
    main()
