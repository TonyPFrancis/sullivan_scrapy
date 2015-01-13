# -*- coding: utf-8 -*-

# Scrapy settings for sullivan_tony project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sullivan_tony'

SPIDER_MODULES = ['sullivan_tony.spiders']
NEWSPIDER_MODULE = 'sullivan_tony.spiders'


ITEM_PIPELINES = {
    'sullivan_tony.pipelines.SullivanTonyPipeline': 1,
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sullivan_tony (+http://www.yourdomain.com)'
