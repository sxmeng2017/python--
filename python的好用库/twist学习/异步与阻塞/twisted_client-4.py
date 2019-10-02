import optparse

from twisted.internet import defer
from twisted.internet.protocol import Protocol, ClientFactory

def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...
    This is the Get Poetry Now! client, Twisted version 4.0
    Run it like this:
      python get-poetry.py port1 port2 port3 ...
    If you are in the base directory of the twisted-intro package,
    you could run it like this:
      python twisted-client-4/get-poetry.py 10001 10002 10003
    to grab poetry from servers on ports 10001, 10002, and 10003.
    Of course, there need to be servers listening on those ports
    for that to work.
    """
    parser = optparse.OptionParser()

    _, addresses = parser.parse_args()

    if not addresses:
        print(parser.format_help())
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr

        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers')
        return host, int(port)

    return [parse_address(i) for i in addresses]


class PoetryProtocol(Protocol):

    poem = ''

    def dataReceived(self, data):
        self.poem += data.decode()

    def connectionLost(self, reason):
        self.poemRecevied(self.poem)

    def poemRecevied(self, poem):
        self.factory.poem_finished(poem)

class PoetryClientFactory(ClientFactory):

    protocol = PoetryProtocol

    def __init__(self, deffered):
        self.deferred = deffered
        """
        这里的self.deffered要在完成整个poem接收后被删去
        原因是保证各个poem使用的self.defer是不同的，但要保证这个效果
        需要强复制，而=只能提供弱复制。如果将d，factory放函数外面
        defer为三首诗共用，所以defer的状态会被共用，一首诗完成后
        会让三首都认为自己完成了，出现输出None的情况。
        所以必须让它们分别有一个defer。
        从这来看，全局只有一个reactor，控制多个defer队列的异步运行。
        而不是一个reactor，有一个defer，这一个defer控制所有程序运行。
        """

    def poem_finished(self, poem):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback(poem)

    def clientConnectionFailed(self, connector, reason):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.errback(reason)

#d = defer.Deferred()
#factory = PoetryClientFactory(d)
def get_poetry(host, port):
    print(port)
    from twisted.internet import reactor
    d = defer.Deferred()
    factory = PoetryClientFactory(d)
    reactor.connectTCP(host, port, factory)
    return d

def poetry_main():
    addresses = parse_args()

    from twisted.internet import reactor

    poems, errors = [], []
    print('start')
    def got_poem(poem):
        print(poem)
        poems.append(poem)
        print('Task ok')
        #reactor.stop()

    def poem_failed(err):
        print('Poem failed:', err)
        errors.append(err)
        #reactor.stop()

    def poem_done(_):
        if len(poems) + len(errors) == len(addresses):
            print('finish')
            print(len(poems))
            reactor.stop()

    for address in addresses:
        print(address)
        host, port = address
        d = get_poetry(host, port)
        d.addCallback(got_poem)
        d.addErrback(poem_failed)
        d.addBoth(poem_done)

    reactor.run()

    #for poem in poems:
    #    print(poem)

if __name__ == '__main__':
    poetry_main()