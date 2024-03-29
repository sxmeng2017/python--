## 学习使用的代码来自
## url: https://github.com/ \
# jdavisp3/twisted-intro/blob/master/blocking-client/get-poetry.py

import datetime, optparse, socket


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...
    This is the Get Poetry Now! client, blocking edition.
    Run it like this:
      python get-poetry.py port1 port2 port3 ...
    If you are in the base directory of the twisted-intro package,
    you could run it like this:
      python blocking-client/get-poetry.py 10001 10002 10003
    to grab poetry from servers on ports 10001, 10002, and 10003.
    Of course, there need to be servers listening on those ports
    for that to work.
    """

    parser = optparse.OptionParser(usage)

    _, addresses = parser.parse_args()

    if not addresses:
        print(parser.format_help())
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.spilt(':', 1)

        if not port.isdigit():
            parser.error('Ports most be integers')

        return host, int(port)

    return [parse_address(i) for i in addresses]


def get_poetry(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    poem = ''

    while True:
        data = sock.recv(1024)

        if not data:
            sock.close()
            break

        poem += data.decode()

    return poem


def format_address(address):
    host, port = address
    return '{0}:{1}'.format(host or '127.0.0.1', port)


def main():
    addresses = parse_args()

    elapsed = datetime.timedelta()

    for i, address in enumerate(addresses):
        addr_fmt = format_address(address)

        print ('Task %d: get poetry from: %s' % (i + 1, addr_fmt))

        start = datetime.datetime.now()

        # Each execution of 'get_poetry' corresponds to the
        # execution of one synchronous task in Figure 1 here:
        # http://krondo.com/?p=1209#figure1

        poem = get_poetry(address)

        time = datetime.datetime.now() - start

        msg = 'Task %d: got %d bytes of poetry from %s in %s'
        print  (msg % (i + 1, len(poem), addr_fmt, time))

        elapsed += time

    print ('Got %d poems in %s' % (len(addresses), elapsed))


if __name__ == '__main__':
    main()
