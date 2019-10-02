##第五个程序小结

该程序给出了两种处理错误
的编程方法。

一种是将错误处理用try-except放入
callback中

一种是将错误处理放入defer的errback

这段程序里最有趣的一段是
random.choice([success, gibberish, bug])()

之后，这个程序有bug，在callback链中第一个是cummingsify
按程序要求，cummingsify出了故障后，如果故障是CannotCummming就
带着诗歌数据，返回callback流。而原程序cummingsify和cummingsify_failed
是同一个stage。Xx_failed不能处理来自cummingsify的结果。如果要满足要求
需要插入一个空函数，或者别的errback。

****纠错****
上面的bug不存在，具体原因见对defer运行程序的测试
