from kafka import KafkaConsumer, KafkaProducer
import sys
import json
from json import loads


bootstrap_servers = ['localhost:9092']
topicName = 'sample-topic'
consumer = KafkaConsumer(topicName, bootstrap_servers = bootstrap_servers, auto_offset_reset = 'earliest', value_deserlizer = lambda x: loads(x.decode('utf-8')))

try:
    for message in consumer:
        print(message.value)
except KeyboardInterrupt:
    sys.exit()


    