import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor

xmlHead = "<?xml version='1.0' encoding='UTF-8'?>\n" \
        "<urlset xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " \
        "xsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9 " \
        "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\" " \
        "xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"

xmlTail = "</urlset></xml>"

class MLSpider(CrawlSpider):
    name = 'mltest'
    allowed_domains = ['marshalorraine.com']
    start_urls = ['http://marshalorraine.com/']
    extractor = SgmlLinkExtractor(allow=('marshalorraine\.com', ), deny_domains=("*.google.*","*.twitter.*")) 
    print xmlHead	
	
    rules = (
        Rule(extractor,callback='parse_links',follow=True),
        )    
	
    def parse_links(self, response):
        respUrl = list()
        for href in response.css('title::text'):
            respUrl.append(response.url)
		
        first = True
        respUrl.sort()
        for urlStr in respUrl:
            if (first):
                print "<url><loc>" + urlStr + "</loc><changefreq>weekly</changefreq></url>"
                first = False
            else:
                print "<url><loc>" + urlStr + "</loc><changefreq>weekly</changefreq></url>"

print xmlTail