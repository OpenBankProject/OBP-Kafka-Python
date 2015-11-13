#!/usr/bin/python

import re
import site 
import obp 

# Use included kafka module
site.addsitedir('lib/')
from kafka import KeyedProducer, KafkaConsumer, KafkaClient


KAFKA_HOST   = "localhost:9092"
TPC_RESPONSE = "Response"
TPC_REQUEST  = "Request"
KAFKA_GRP_ID = "0"
DEBUG        = False


# Split message and extract function name and arguments
# then pass them to obp.py for further processing 
#
def processMessage(message):
  reqFunc = None 
  reqArgs = None 
  rFnc = re.match("^(.*?):", message)
  if rFnc != None:
    reqFunc = rFnc.group(1)
  rArg = re.findall("{+(.*?):(.*?)}+", message)
  if rArg != None:
    reqArgs = dict((k, v) for (k, v) in rArg)
  if reqFunc == None:
    return '{"error":"empty request"}'
  if not re.match("^[a-zA-Z0-9_-]*$", reqFunc):
    return '{"error":"llegal request"}'
  if (hasattr(obp, reqFunc)):
    return getattr(obp, reqFunc)(reqArgs)
  else:
    return '{"error":"unknown request"}'


# Main loop waits indefinitely for requests 
# then passes them to processMessage()
#
producer = KeyedProducer( KafkaClient(KAFKA_HOST) )
consumer = KafkaConsumer( TPC_REQUEST,
                          group_id=KAFKA_GRP_ID,
                          bootstrap_servers=[KAFKA_HOST])
for message in consumer:
  if (DEBUG):
    print("%s:%d:%d: key=%s value=%s" % ( message.topic, 
                                          message.partition,
                                          message.offset,
                                          message.key,
                                          message.value))
  result = processMessage(message.value)
  print result
  if result != None:
    producer.send_messages( TPC_RESPONSE.encode("UTF8"), 
                            message.key,
                            result.encode("UTF8"))
   
