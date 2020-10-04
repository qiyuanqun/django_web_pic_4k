'''
网络编程：实现进程间的通信


基本概念：

    一个程序如何在网络上找到另一个程序？

        首先，程序必须启动；其次，必须有程序所在电脑的地址（ip），通过地址找到电脑，再通过端口找到电脑上具体的程序

    ip地址精确到具体的一台电脑，端口精确到电脑上具体的程序

    Linux查看网卡信息：ifconfig

    windows查看网卡信息：ipconfig

    本地环回：127.0.0.1

    ip地址包括：网络号和主机号（根据网络号可知是否处于同一局域网）

    ipv4：4组0~255的数字组成

    ipv6：ipv4被用完了，新版本

    端口：在linux上有2的16次方个端口号，其中0~1023为知名端口，1024及之后为动态端口

    进程：运行的程序以及运行时用到的资源(地址空间、内存、数据栈等)

    进程间通信：每个进程都有自己的数据栈，只能使用进程间通信，而不能共享信息

    socket（套接字）：是实现进程间通信的一种方式，它与其他进程间通信方式的一个主要不同在于：它能实现不同主机间的进程间通信
'''


'''
通信的两种方式——UDP和TCP

    UDP——用户数据报协议，是一种简单的面向数据报的运输层协议；
        
        它不提供可靠性，只负责发送数据，不能保证一定到达目的地；
        
        由于传输数据前不用在客户端和服务端建立连接，且没有超时重发等机制，故传输速度快

    TCP——传输控制协议，提供面向连接、可靠的服务；
        
        在客户端和服务器彼此交换数据前，必须先在双方之间建立一个TCP连接，之后才能进行数据传输；
        
        TCP提供超时重发、丢弃重复数据、校验数据等功能，保证数据一定到达
'''

# udp_recv_demo.py  运行时先接收数据的一方先运行

import socket


def main():
    '''接收数据整体控制'''
    # 创建套接字
    udp_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定ip和端口号
    udp_recv_socket.bind(('',7788))

    # 返回一个元组：(接收到的bytes类型数据, ('发送方的ip', 发送方端口号))
    recvdata = udp_recv_socket.recvfrom(1024)  # 一次接收的最大内存
    
    # 接收时未解码的bytes类型数据包含的中文字符打印时以进制形式展示，如b'\xe8\xbe\x89\xe7\x85\x8c\xe7\xa7\x91\xe6\x8a\x80'
    print(recvdata)

    # 关闭套接字
    udp_recv_socket.close()


if __name__ == '__main__':
    main()


# udp_send_demo.py

import socket


def main():
    '''发送数据主体控制'''
    # 创建套接字
    udp_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 发送  两个参数：bytes类型数据，('ip地址',端口号)
    # bytes类型数据：对于ASCII字符(英文)组成的字符串，可在字符串前直接加上b，也可以编码，对于包含中文字符的字符串，只能将其编码为bytes类>    型才能传输
    udp_send_socket.sendto('辉煌科技'.encode('utf-8'),('127.0.0.1', 7788))
    
    # 关闭套接字
    udp_send_socket.close()


if __name__ == '__main__':
    main()


'''
windows系统默认gbk编码，接收从Windows发送过来的数据要gbk解码

单工：百分百只能单向传递

半双工：可以双向，但是同一时刻只能向一个方向传递

全双工：同一时刻既能接收又能发送

recvfrom()：程序从操作系统中拿数据，有就拿，没有就等；如果没有接收的功能，而另外的程序一直给该程序发消息，会卡死    
'''


# tcp_server_demo.py

import socket


def main():
    '''整体控制'''
    # 创建服务器套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    # 绑定本地信息  参数为元组
    tcp_server_socket.bind(('',7788))

    # 变主动套接字为被动 这个参数没实际意义，用128即可，表示一次最多为128个客户端服务
    tcp_server_socket.listen(128)

    # 等待新的客户端连接，返回一个元组：(并专门为到达的客户端创建的新套接字服务, 到达的客户端信息——ip和端口元组)
    new_client_socket, new_client_addr = tcp_server_socket.accept()
    print(new_client_addr)

    # 接收数据  仅返回数据字节流(因为上面已经知道客户端信息了)
    recv_data = new_client_socket.recv(1024)

    # 发送数据  同理，只需字节流数据参数
    new_client_socket.send('已经收到数据'.encode('utf-8'))
    
    # 关闭套接字
    new_client_socket.close()
    tcp_server_socket.close()


if __name__ == '__main__':
    main()


# tcp_client_demo.py

import socket


def main():
    # 创建套接字
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接服务器  参数为元组
    tcp_client_socket.connect(('127.0.0.1', 7788))

    # 发送数据
    tcp_client_socket.send('向服务器发送数据'.encode('utf-8'))

    # 接收数据
    recv_data = tcp_client_socket.recv(1024)
    print(recv_data.decode('utf-8'))

    # 关闭套接字
    tcp_client_socket.close()


if __name__ == '__main__':
    main()


'''
如果recv解堵塞，有两种可能：
    
    1、客户端发送过来数据
    
    2、客户端调用close导致，此时recv到的数据为空，可用于判断是否为客户端服务完毕

客户端不需要绑定端口，如QQ
'''
'''
