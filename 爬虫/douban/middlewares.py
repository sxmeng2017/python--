from scrapy import signals


class DoubanSpiderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        ## 这个方法被用于创建spider
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        ## 用于处理传递给spider的每个响应
        ## 应该返回None,或者产生个exception

        return None

    def process_spider_output(self, response, result, spider):
        ## 处理所有spider处理后的数据
        ## 必须返回一个可迭代的请求，字典或者item类别

        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        ## 当spider或者process_spider_input方法报错时
        ## 产生一个exception

        ## 该方法应该返回None或者可迭代的响应，字典，item
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class DoubanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # curl https://m.douban.com/book/subject/26628811/ -x http://127.0.0.1:8081
        request.meta['proxy'] = 'http://127.0.0.1:8081'
        # request.meta['proxy'] = 'http://10.0.0.164:1080'

