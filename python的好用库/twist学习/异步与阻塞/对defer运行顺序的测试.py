from twisted.internet import defer

d = defer.Deferred()

def call1(_):
    print('call1')
    raise ValueError('call1')

def call2(_):
    print('call2')

def err1(_):
    print('err1')

def err2(_):
    print('err2')

from twisted.internet import reactor

d.addCallbacks(call1, err1)
# d.addCallback(call1)
# d.addErrback(err1)
d.addCallbacks(call2, err2)
# d.addCallback(call2)
print('ok')

d.callback('0')
# d.errback(ValueError('0'))

"""
这是一个defer的测试，从这里看addCallback和adderrbeck
都有添加一整个stage的作用
在addCallback(call1)之后addErrback(err1)，程序会从call1，流动到
err1，而addCallbacks(call1, err1)，就不会。这说明
addCallback与addErrback都是使用addCallbacks的
又由在addCallback(call1)之后addErrback(err1)时，
d.errback(ValueError('0'))还是会从err1流过。
所以填补每个stage的空白的应该是一个只传递参数的函数。
查看源码，也确实如此
    def passthru(arg):
        return arg

    def addCallbacks(self, callback, errback=None,
                     callbackArgs=None, callbackKeywords=None,
                     errbackArgs=None, errbackKeywords=None):
        
        assert callable(callback)
        assert errback is None or callable(errback)
        cbs = ((callback, callbackArgs, callbackKeywords),
               (errback or (passthru), errbackArgs, errbackKeywords))
        self.callbacks.append(cbs)

        if self.called:
            self._runCallbacks()
        return self


    def addCallback(self, callback, *args, **kw):
        
        return self.addCallbacks(callback, callbackArgs=args,
                                 callbackKeywords=kw)


    def addErrback(self, errback, *args, **kw):
        
        return self.addCallbacks(passthru, errback,
                                 errbackArgs=args,
                                 errbackKeywords=kw)


    def addBoth(self, callback, *args, **kw):
        
        return self.addCallbacks(callback, callback,
                                 callbackArgs=args, errbackArgs=args,
                                 callbackKeywords=kw, errbackKeywords=kw)

"""
