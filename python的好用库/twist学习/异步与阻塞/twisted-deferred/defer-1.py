from twisted.internet.defer import Deferred
def get_poem(res):
    print('Your poem is served: ')
    print(res)

def poem_failed(err):
    print(err.__class__)
    print(err)
    print('No poetry for you')

d = Deferred()
d.addCallbacks(get_poem, poem_failed)
# d.callback('This poem is short')
# d.callback('second result')
print('Finish')

print('*'*15)

d.errback(Exception('i have failed'))
"""
注意这里callback和errback不能都被调用，一个被调用了，另一个就不能被调用
同时callback也不能激活两次
"""
