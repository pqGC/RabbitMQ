import pika

creds_broker = pika.PlainCredentials("test", "123456")
# 定义连接池
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, credentials=creds_broker))
# 创建一个消息通道
channel = connection.channel()
# 创建一个消息队列，消息队列的名称为task_queue，
# 这里的第二个参数durable，是对消息队列的设置，
# 使得RabbitMQ在发生异常退出时发送的消息不会被丢失，该消息会被发送给其他消费者
channel.queue_declare(queue='mytest')
for i in range(10):
    channel.basic_publish(exchange='', routing_key='mytest', body=str(i),  # 注意当未定义exchange时，routing_key需和queue的值保持一致
                          properties=pika.BasicProperties(delivery_mode=2))  # mode>=2表示消息的持久化
    print('send success msg to rabbitmq   msg--->{}'.format(i))
connection.close()   # 关闭连接
