import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
#from apesmit import Sitemap

xmlHead = "<?xml version='1.0' encoding='UTF-8'?>\n" \
        "<urlset xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " \
        "xsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9 " \
        "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\" " \
        "xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"

xmlTail = "</urlset></xml>"

class WiProSpider(CrawlSpider):
    name = 'wiprositemap'
    allowed_domains = ['wiprodigital.com']
    start_urls = ['http://wiprodigital.com/']
    extractor = SgmlLinkExtractor(allow=('wiprodigital\.com', ), deny_domains=("*.google.*","*.twitter.*")) 
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

#sm=Sitemap(changefreq='weekly')
#sm.add('http://www.wiprodigital.com/')
#out=open('sitemap.xml', 'w')
#sm.write(out)
#out.close()
	
# filename = response.url.split("/")[-2] + '.html'
    #with open(filename, 'wb') as f:
    #    f.write(response.body)