import time
import pika


creds_broker = pika.PlainCredentials("test", "123456")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, credentials=creds_broker))
channel = connection.channel()

channel.queue_declare(queue='mytest')


def callback(ch, method, properties, body):
    '''
    回调函数,处理从rabbitmq中取出的消息
    '''
    print(" [x] Received %r" % body)
    # time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 发送ack消息


# 添加不按顺序分配消息的参数===>先来先得
# 设置每一个消费者最大的消息处理数量，这里设置为1个
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='mytest', no_ack=False)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()  # 开始监听 接受消息
