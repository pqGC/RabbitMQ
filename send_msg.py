import pika

creds_broker = pika.PlainCredentials("test", "123456")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, credentials=creds_broker))     # 定义连接池
channel = connection.channel()
channel.queue_declare(queue='mytest')    # 声明队列以向其发送消息消息
for i in range(1000):
    channel.basic_publish(exchange='', routing_key='mytest', body=str(i),  # 注意当未定义exchange时，routing_key需和queue的值保持一致
                          properties=pika.BasicProperties(delivery_mode=2))  # mode>=2表示消息的持久化
print('send success msg to rabbitmq')
connection.close()   # 关闭连接
