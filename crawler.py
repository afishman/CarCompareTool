import urllib2

class Crawler:
    def get_html(url):
    request = urllib2.urlopen(url, context=ssl._create_unverified_context())
    return request.read()

    @abstractmethod
    def crawl()

    