## 学习使用的代码来自
## https://blog.csdn.net/m0_37717595/article/details/80603884
## https://docs.python.org/3/library/optparse.html

from optparse import OptionParser


def main():
    opt = OptionParser()
    opt.add_option('-f', '--file', action='store', type='string', dest='filename')
    opt.add_option('-v', '--version', action='store_false', dest='verbose', default='hello',
                help='version')
    opt.add_option('-n', '--name', action='store', type='string', dest='name')
    opt.add_option('-o', '--operate', action='store', dest='operate')

    #arg = ['-f', 'file.txt','-v', 'how are you', 'arg1', 'arg2']
    options, args = opt.parse_args()
    #op, ar = opt.parse_args(arg)
    print('options:', options)
    print('args:', args)
    #print('op:', op)
    #print('ar:', ar)
    #if len(args) != 1:
    #    opt.error('you have wrong input')
    if not options.operate:
        opt.error('not operate')
    print(options.operate)


if __name__ == '__main__':
    main()
