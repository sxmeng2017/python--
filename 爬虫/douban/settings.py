BOT_NAME =  'douban'

SIPDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

LOG_LEVEL = 'DEBUG'
IMAGES_STORE = '../storage/'

ITEM_PIPELINES = {
    'douban.pipelines.CoverPipeline': 1,
    'douban.pipelines.DoubanPipeline': 300,
}

