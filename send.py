import pika
import keys
from pip._vendor.distlib.compat import raw_input

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',  exchange_type='fanout')

choices = [keys.CSV, keys.JSON, keys.SQL, keys.XML]
for choice in choices:
    print(choice)

answers = raw_input('Enter your choice : ')

while answers not in choices:
    print("Please select from the list")
    answers = raw_input('Enter your choice : ')

message = keys.PATH + "  " + answers
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

print(" [x] Sent %r" % message)
connection.close()