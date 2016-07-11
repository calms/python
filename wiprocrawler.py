import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor

class WiProSpider(CrawlSpider): 
    name = 'wiprocrawl' 
    allowed_domains = ['wiprodigital.com'] # domains to follow
    start_urls = ['http://wiprodigital.com/'] # sites to crawl
    
    extractor = SgmlLinkExtractor(allow=('wiprodigital\.com', ), deny_domains=("*.google.*","*.twitter.*")) # crawl should exclude google & twitter links

    rules = (
        Rule(extractor,callback='parse_links',follow=True),
       )
		
    
    def parse_links(self, response): # parse web pages for title, image links and urls
        for href in response.css('title::text'):
            yield {'Title':  response.css('title::text').extract_first(),
                'URL': response.url				
            }
            yield {'Image Link': response.css('img::attr(src)').extract()}
