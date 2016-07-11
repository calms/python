


   ===-----===




GitHub Links:


Python Web Crawler Solution

wiprocrawler.py

- https://github.com/calms/python/blob/master/wiprocrawler.py

Json Output Example:

- https://github.com/calms/python/blob/master/wiprocrawl.json




Python Sitemap Solution

wiprocrawlerSitemap.py

- https://github.com/calms/python/blob/master/wiprocrawlerSitemap.py

Sitemap Output Example:

- https://github.com/calms/python/blob/master/wiprositemap.xml


   ===-----===


Install Python

- https://www.python.org/downloads/
- http://docs.python-guide.org/en/latest/starting/install/win/


Install scrapy (this can be done using "pip install scrapy")

- http://doc.scrapy.org/en/latest/intro/install.html


Other modules that you may need to install incude Twisted (13.1.0), pypiwin32, service_identity (16.0.0), zope.interface (3.6.1) and crytography.



   ===-----===



Command to run & generate json file of titles and links (includes image link): 

- scrapy crawl wiprocrawl -o wiprocrawl.json -t json



Commands to create, run & generate xml file of Sitemap: 

- scrapy genspider wiprositemap spiders\wiprocrawlerSitemap.py

- scrapy crawl wiprositemap 1>wiprositemap.xml

