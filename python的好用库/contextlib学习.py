from contextlib import contextmanager


## 先给一个最基础的with方法的使用,
## 以下代码实例转载于url:https://www.cnblogs.com/pyspark/articles/8819803.html

class OpenContext():

    def __init__(self, filename, mode):
        self.fp = open(filename, mode)

    def __enter__(self):
        return self.fp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()


## with OpenContext('filename','a') as file_obj:
##     file_obj.write('hello')


## 以下为使用contextlib的例子

class MyResource:
    def query(self):
        print("query data")


@contextmanager
def make_myresource():
    print("connect to resource")
    yield MyResource()
    print("over")

with make_myresource() as r:
    r.query()


## 实例2

## 有些时候我们需要对输出结果进行一点修饰


@contextmanager
def book_mark():
    print('《', end='')
    yield
    print('》', end='')

with book_mark():
    print("时代的尘埃", end='')


## 案例三

##如果数据库有提交的操作需要重复，但这些操作基本一样，重复太多

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

class SQLAIchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e



