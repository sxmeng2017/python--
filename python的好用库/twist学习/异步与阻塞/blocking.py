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

    _, addresses