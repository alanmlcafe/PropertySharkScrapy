# -*- coding: utf-8 -*-

# Scrapy settings for propertyshark project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'propertyshark'

SPIDER_MODULES = ['propertyshark.spiders']
NEWSPIDER_MODULE = 'propertyshark.spiders'

CONCURRENT_REQUESTS_PER_IP = 1

#Export as CSV Feed
FEED_FORMAT = "csv"
FEED_URI = "tmp/property.csv"

#write all csv files without headers.
FEED_EXPORTERS = {
    'csv': 'propertyshark.exporters.HeadlessCsvItemExporter',
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'propertyshark (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Retry many times
RETRY_ENABLED = True
RETRY_TIMES = 20

#=========================================================
#====================PROXY MIDDLEWARE=====================
#=========================================================


# Retry on most error codes since proxies fail for different reasons
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
#     'scrapy_proxies.RandomProxy': 100,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
# }

# PROXY_LIST = '/proxy/proxylist.txt'

#=========================================================
#==================PROXY MIDDLEWARE END===================
#=========================================================