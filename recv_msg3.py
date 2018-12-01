import gevent
import time
import pika
from gevent import monkey
monkey.patch_socket()
from urllib import request
from multiprocessing.pool import Pool


def test_gevent(i):
    """
    多线程内嵌gevent的测试
    """
    print('[*]process{} start...'.format(i))
    creds_broker = pika.PlainCredentials("test", "123456")
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='127.0.0.1', port=5672, credentials=creds_broker))
    channel = connection.channel()
    channel.queue_declare(queue='mytest')

    def callback(ch, method, properties, body):
        """
        回调函数,处理从rabbitmq中取出的消息
        """
        print(" [process{}] Received {}".format(i, body))
        try:
            # time.sleep(3)
            dowork(i, ch, method, body)
        finally:
            print('         [process {}] work {} Finished!'.format(i, body))
            ch.basic_ack(delivery_tag=method.delivery_tag)  # 发送ack消息

    def dowork(i, ch, method, body):
        urls = ['http://www.cnblogs.com/God-Li/p/7774497.html', 'http://www.gevent.org/', 'https://www.python.org/']
        # url = random.choice(urls)
        # gevent.spawn(func, url)
        task_list = list()
        for url in urls:
            task_list.append(gevent.spawn(func, url, i, body))
        gevent.joinall(task_list)
        # res = request.urlopen(url)
        # data = res.read()
        # if res.code == 200:
        #     print('     [+]process {} work {}->{} Done！'.format(i, body, url))
        # else:
        #     print('     URL EOF!')

    def func(url, i, body):
        res = request.urlopen(url)
        time.sleep(1)
        if res.code == 200:
            print('     [+]process {} work {}->{} Done！'.format(i, body, url))
            # print('work {} Done!'.format(body))
            # ch.basic_ack(delivery_tag=method.delivery_tag)  # 发送ack消息
        else:
            print('URL EOF!')

    # 添加不按顺序分配消息的参数===>先来先得
    # 设置每一个消费者最大的消息处理数量，这里设置为1个
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='mytest', no_ack=False)
    channel.start_consuming()  # 开始监听 接受消息


if __name__ == '__main__':
    p = Pool()
    for i in range(5):
        p.apply_async(test_gevent, args=(i,))
    p.close()
    p.join()
