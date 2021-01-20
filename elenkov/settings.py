BOT_NAME = 'elenkov'
SPIDER_MODULES = ['elenkov.spiders']
NEWSPIDER_MODULE = 'elenkov.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
ITEM_PIPELINES = {
    'elenkov.pipelines.DatabasePipeline': 300,
}
