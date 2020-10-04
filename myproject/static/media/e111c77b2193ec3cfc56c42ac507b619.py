'''
基本概念
    
    什么是进程？

        运行的程序以及运行时用到的资源(地址空间、内存、数据栈等)
       
        所以进程是资源分配的单位

    什么是线程？
        
        操作系统能够进行运算调度的最小单位
        
        它被包含在进程之中，依赖于进程，是进程中的实际运作单位。
        
        一条线程指的是进程中一个单一顺序的控制流，一个进程中可以并发多个线程，每条线程并行执行不同的任务

        一个进程中的各个线程之间共享同一片数据空间，但是这样的共享会面临资源竞争

    并发：任务数多于CPU核数，操作系统轮流让各任务交替执行，切换速度相当快，看上去像是一起执行

    并行：任务数小于等于CPU核数，任务真的一起执行

    全局解释器锁GIL：保证同一时刻只有一个线程在运行
'''


# 直接使用threading.Thread类
# threading_demo.py

import threading
import time


def test1(num):
    for i in range(10):
        print(i+num)
        time.sleep(1)


def test2(num):
    for i in range(10):
        print(i + num)
        time.sleep(1)


def main():
    '''整体流程控制'''
    thread_1 = threading.Thread(target=test1, args=(10,))  # 函数参数用元组传递，单个参数后面加逗号
    thread_2 = threading.Thread(target=test2, args=(100,))
    thread_1.start()
    thread_2.start()

if __name__ == '__main__':
    main()


# 继承threading.Thread类方式
# mythread_demo.py

import threading
import time


class MyThread(threading.Thread):
    def __init__(self, num):
        super(MyThread, self).__init__()
        self.num = num

    # 必须定义run()方法
    def run(self):
        for i in range(10):
            print(i + self.num)
            time.sleep(1)

    # 封装其他函数       
    def other_function(self):
        pass


def main():
    '''整体流程控制'''
    t1 = MyThread(10)
    t2 = MyThread(100)
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()


'''
global的使用，当有全局变量时num，想在函数中修改全局变量的值（实质是改变num的指向）时，可用global num = 10

多线程共性全局变量时的问题————资源竞争
    
    有全局变量num = 0

    线程1和线程2同样操作：对 num+=1 进行for循环

    num+=1 其实为3步：第一，获取num的值；第二，把值加1；第三，将值存到num

    而在线程切换时并不能保证这三步都完成了

同步：协同步调（一个一个来）

线程同步：解决资源竞争————互斥锁

    创建锁：mutex = threading.Lock()

    将合适的地方用锁给锁定：mutex.acquire()

    将锁释放：metux.release()

如果没理清应该在哪里上锁，在哪里释放锁，可能会出现死锁（都需要等待对方释放锁，堵塞）的情况
'''


'''
子进程资源从主进程复制而来，虽是复制，但还是有些区别如进程号
'''


# multiprocessing_demo.py

import multiprocessing
import time


def test1(num):
    for i in range(10):
        print(i+num)
        time.sleep(1)


def test2(num):
    for i in range(10):
        print(i + num)
        time.sleep(1)


def main():
    p1 = multiprocessing.Process(target=test1, args=(10,))
    p2 = multiprocessing.Process(target=test2, args=(100,))
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()


'''
通过队列可实现  同一电脑上  进程间通信，队列起到解耦作用

不同电脑上进程通信用redis
'''


# mul_queue_demo.py

import multiprocessing
import time


def download_from_web(q):
    '''下载数据'''
    # 模拟从网上下载的数据
    data = [11,22,33,44]

    for temp in data:
        # 向对列中写数据
        q.put(temp)

    print('下载结束')


def analysis(q):
    '''数据处理'''
    waitting_analysis_data = list()  # 空列表用list()可读性强

    while True:
        # 从队列中获取数据
        data = q.get()
        waitting_analysis_data.append(data)
        if q.empty():
            break

    # 模拟数据处理
    print(waitting_analysis_data)


def main():
    # 创建一个队列
    q = multiprocessing.Queue(3)  # 3代表队列最多存放3个数据，不写则由操作系统决定

    # 创建多进程，将队列的引用当做实参传入
    p1 = multiprocessing.Process(target=download_from_web,args=(q,))
    p2 = multiprocessing.Process(target=analysis, args=(q,))
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()


'''
多进/线程中当进程数很多时用进/线程池，以避免新建太多进/线程对象，实际开发中进/线程池包含多少个进/线程要进过测试才知道
'''


# mul_pool_demo.py

import multiprocessing


def test(num):
    print(num)


def main():
    # 创建进程池  参数为最大进程数
    po = multiprocessing.Pool(5)

    # 向进程池中添加任务
    for i in range(10):
        po.apply_async(test, args=(i,))

    # 关闭进程池，不再接收新的请求
    po.close()

    # 告诉主进程等待子进程结束，必须在close()之后
    po.join()

if __name__ == "__main__":
    main()


# mul_pool_copy_file_or_dir_demo.py

import multiprocessing
import os
import time


def copyfile(file_path, dir_path):
    file_name = os.path.basename(file_path)  # 文件名

    save_file_path = '/'.join([dir_path, file_name])  # 存储文件路径

    with open(file_path, 'rb') as f:
        with open(save_file_path, 'ab') as s:
            for line in f:
                s.write(line)


def copyhandler(po, file_or_dir_path, dir_path):
    '''处理文件或文件夹'''
    if os.path.exists(file_or_dir_path):
        if os.path.isfile(file_or_dir_path):
            # 是文件
            po.apply_async(copyfile, args=(file_or_dir_path, dir_path))

        if os.path.isdir(file_or_dir_path):
            # 是文件夹
            dir_name = os.path.basename(file_or_dir_path)
            dir_path = '/'.join([dir_path, dir_name])

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            filename_list = os.listdir(file_or_dir_path)

            for filename in filename_list:
                file_path = '/'.join([file_or_dir_path, filename])
                copyhandler(po, file_path, dir_path)
    else:
        print('路径不存在')


def main():
    old_file_or_dir_path = '/home/luoguifu/个人笔记文件/python高级/demo'
    save_dir_path = '/home/luoguifu/个人笔记文件/python高级/复制的文件'

    po = multiprocessing.Pool(5)
    copyhandler(po, old_file_or_dir_path, save_dir_path)
    po.close()
    po.join()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end - start)




'''
协程--yield--人工切换
    
    task1()...yield...  task2()...yield...
    t1=task1()  t2=task2(  
    # 实现交替执行)
    while True:
        next(t1)  # 迭代器除了for循环一个一个取出，还可以用next()一次取出一个结合循环使用
        next(t2)

协程依赖于线程，这里手动切换，在遇到耗时操作时切换，充分利用线程，消耗资源最少

协程--greenlet(pip安装)--人工切换
    from greenlet import greenlet
    函数1中：
        gr2.switch()  # 手动切换到函数2
    函数2中：
        gr1.switch()
    gr1 = greenlet(函数名1)  # 参数靠switch(传入位置参数值)  [gr.switch(*args, **kwargs): 切换到gr协程]
    gr2 = greenlet(函数名2)
    g1.switch()  # 让协程g1先抢占cpu资源
    
协程--gevent(pip安装)－－自动切换
    
    操作非常耗时，经常使程序处于等待状态，gevent会自动切换

    import gevent
    g1 = gevent.spawn(函数名,参数1，参数2。。。)  # 此时不执行
    g1.join()  # 等g1执行，遇到阻塞时切换，没阻塞不切换

    gevent中延时不用time.sleep(),用gevent.sleep()，或
    from gevent import monkey
    monkey.patch_all()

    进程切换耗费资源相当大，线程次之，协程(相当于调用了一个函数)最小

    协程很多时，用gevent.joinall([gevent.spawn(f1,参数),gevent.spawn(f2,参数)...])

    协程依赖于线程，是并发
'''
