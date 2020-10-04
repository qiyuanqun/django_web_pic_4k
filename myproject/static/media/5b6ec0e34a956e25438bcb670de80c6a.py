'''
对list、str、tuple等类型的数据用for循环依次从中拿到数据进行使用的过程，这样的过程叫遍历，也叫迭代。这样的类型叫可迭代对象

迭代是访问序列元素的一种方式

迭代器是一个可以记住遍历的位置的对象，从集合的第一个开始访问，直到所有元素被访问结束，只能往前不能后退

isinstance([], Iterable/Iterator)  在collections模块中

让一个类实例对象(属性name = list())可用for循环遍历出来

    若类中有__iter__(self)，则类实例是可迭代对象，该方法返回一个迭代器对象
    
    若除了__iter__(self)，类中还有__next__(self)，则类对象是一个迭代器

迭代器的使用：数据什么时候用，什么时候生成数据，保存的是数据生成方式，而不是结果

    迭代器通过 StopIteration 异常标识迭代的完成

    如：fibonacci数列

        若用列表存储，则占空间

        若用迭代器（创建一个迭代器类，内部是生成数列的算法），则数据用时在生成，不占空间
'''


class Fibonacci(object):
    def __init__(self,all_num):
        self.all_num = all_num
        self.current_num = 0
        self.a = 0
        self.b = 1

    def __iter__(self):
        ''' 如果要一个对象称为可迭代对象 即可以使用for， 那么必须实现__iter__方法'''
        return self

    def __next__(self):
        if self.current_num < self.all_num:
            ret = self.a
            self.a, self.b = self.b, self.a + self.b
            self.current_num += 1
            return ret
        else:
            raise StopIteration  # 标识迭代完成


fibo = Fibonacci(10)
for num in fibo:
    print(num)


'''
生成器：一种特殊的迭代器
    
    类似列表生成式，(i for i in range(10))

    函数中有yield,遇到yield返回，下次执行时接着yield继续，（此时已经不是函数，而是一个生成器模板）（调用如同调用函数形式一样，但已经不是调用函数而是创建一个生成器对象）
'''


# generator_demo.py
from collections import Iterable, Iterator


def generator(num):
    '''生成从0到num的序列'''
    current_num = 0
    while True:
        if current_num <= num:
            yield current_num
            current_num += 1
        else:
            raise StopIteration


if __name__ == '__main__':
    a = (i for i in range(10))
    for i in a:
        print(i)

    g = generator(10)
    print(isinstance(g, Iterable))  # True
    print(isinstance(g, Iterator))  # True
    for i in g:
        print(i)

