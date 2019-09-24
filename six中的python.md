##这里记录的是有关six的学习

####运行环境

six.PY2 返回一个表示当前运行环境是否为python2的bool值

six.PY3 同理

####常量

six.class_types

这里主要是针对python中的old-style和new-style。py2两者都有，py3中只有new
两者的区别如下

如果有一个实例x，old-style中x.__class__为x的类名，type(x)为<type
  'instance'>.
  
new-style则两者一致为x.__class__
  
new的出现是为了提供一个确认子类的方式，用处很大（雾）
  
six.integer_types

py2中有int和long两种整数类型,py3只有int

six.string_types

字符串类型，py2中为basestring，py3位str

six.text.types

文本字符类型，2中为Unicode，3中为str

six.binary_types

字节序列类型，2中为str，3中bytes

###注意！！！

Python2 中字符的类型：

str： 已经编码后的字节序列

unicode： 编码前的文本字符


Python3 中字符的类型：

str： 编码过的 unicode 文本字符

bytes： 编码前的字节序列

我们可以认为字符串有两种状态，即文本状态和字节（二进制）状态。
Python2 和 Python3 中的两种字符类型都分别对应这两种状态，
然后相互之间进行编解码转化。
编码就是将字符串转换成字节码，涉及到字符串的内部表示；解码就是将字节码转换为字符串，将比特位显示成字符。

在 Python2 中，str 和 unicode 都有 encode 和 decode 方法。但是不建议对 str 使用 encode，对 unicode 使用 decode, 
这是 Python2 设计上的缺陷。Python3 则进行了优化，str 只有一个 encode 方法将字符串转化为一个字节码，
而且 bytes 也只有一个 decode 方法将字节码转化为一个文本字符串。

Python2 的 str 和 unicode 都是 basestring 的子类，所以两者可以直接进行拼接操作。而 Python3 中的 bytes 和 str 是两个独立的类型，两者不能进行拼接。

Python2 中，普通的，用引号括起来的字符，就是 str；此时字符串的编码类型，对应着你的 Python 文件本身保存为何种编码有关，
最常见的 Windows 平台中，默认用的是 GBK。Python3 中，被单引号或双引号括起来的字符串，就已经是 Unicode 类型的 str 了。
对于 str 为何种编码，有一些前提：

Python 文件开始已经声明对应的编码

Python 文件本身的确是使用该编码保存的

两者的编码类型要一样（比如都是 UTF-8 或者都是 GBK 等）

在 Python3 中，字符编码问题得到了极大的优化，不再像 Python2 那么头疼。
在 Python3 中，文本总是 Unicode, 由 str 类型进行表示，二进制数据使用 bytes 进行表示，
不会将 str 与 bytes 偷偷的混在一起，使得两者的区别更加明显。



