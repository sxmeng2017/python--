"""
这段代码和第二个版本的代码的区别在于使用了回调函数来处理
接受的结果。这样讲回调单独独立出来对代码的复用有较好的好处。

但代码中其他关于程序运行的提示信息全部被删了，尤其get_poetry
如果是在该函数内部初始化，不知道factory还是不是共用一个，
直接在2的基础上改写不行。

要改写要把该工厂的初始化放外面。
"""




import datetime, optparse

from twisted.internet.protocol import Protocol, ClientFactory



def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...
    This is the Get Poetry Now! client, Twisted version 1.0.
    Run it like this:
      python get-poetry.py port1 port2 port3 ...
    If you are in the base directory of the twisted-intro package,
    you could run it like this:
      python twisted-client-1/get-poetry.py 10001 10002 10003
    to grab poetry from servers on ports 10001, 10002, and 10003.
    Of course, there need to be servers listening on those ports
    for that to work.
    """

    parser = optparse.OptionParser(usage=usage)

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

    return [parse_address(addr) for addr in addresses]

class PoetryProtocol(Protocol):

    poem = ''

    def dataReceived(self, data):
        self.poem += data

    def connectionLost(self, reason):
        self.poemReceived(self.poem)

    def poemReceived(self, poem):
        self.factory.poem_finished(poem)


class PoetryClientFactory(ClientFactory):

    protocol = PoetryProtocol

    def __init__(self, callback):
        self.callback = callback

    def poem_finished(self, poem):
        self.callback(poem)


def get_poetry(host, port, callback):
    """
    Download a poem from the given host and port and invoke
      callback(poem)
    when the poem is complete.
    """
    from twisted.internet import reactor
    factory = PoetryClientFactory(callback)
    reactor.connectTCP(host, port, factory)


def poetry_main():
    addresses = parse_args()

    from twisted.internet import reactor

    poems = []

    def got_poem(poem):
        poems.append(poem)
        if len(poems) == len(addresses):
            reactor.stop()

    for address in addresses:
        host, port = address
        get_poetry(host, port, got_poem)

    reactor.run()

    for poem in poems:
        print(poem)



if __name__ == '__main__':
    poetry_main()