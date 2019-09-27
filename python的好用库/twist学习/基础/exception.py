def falldown():
    raise Exception('i fall down')

def upagain():
    print('But i get up again')
    reactor.stop()


from twisted.internet import reactor

reactor.callWhenRunning(falldown)
reactor.callWhenRunning(upagain)


print('starting the reactor')
reactor.run()