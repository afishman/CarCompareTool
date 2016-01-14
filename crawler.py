import urllib2
from abc import ABCMeta, abstractmethod
import ssl

class Crawler:

    def get_html(self, url):
        request = urllib2.urlopen(url, context=ssl._create_unverified_context())
        return request.read()

    @abstractmethod
    def crawl(self):
        raise NotImplementedError()

