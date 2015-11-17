#!/usr/bin/python

import re
import site 
import obp 

# Use included kafka module
site.addsitedir('lib/')
from kafka import KeyedProducer, KafkaConsumer, KafkaClient

# Define globals
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
  # regex match function name
  rFnc = re.match("^(.*?):{", message)
  if rFnc != None:
    reqFunc = rFnc.group(1)
  # regex match function arguments
  rArg = re.findall("[{,](.*?):\"(.*?)\"", message)
  # create dictionary if not empty
  if rArg != None:
    reqArgs = dict((k, v) for (k, v) in rArg)
  # return error if empty
  if reqFunc == None:
    return '{"error":"empty request"}'
  # return error if function name if not alphanumeric 
  if not re.match("^[a-zA-Z0-9_-]*$", reqFunc):
    return '{"error":"llegal request"}'
  # check if function name exists in obp.py
  if (hasattr(obp, reqFunc)):
    # execute function from obp.py and return result
    return getattr(obp, reqFunc)(reqArgs)
  else:
    return '{"error":"unknown request"}'


# Main loop waits indefinitely for requests 
# then passes them to processMessage()
#

# init kafka producer
producer = KeyedProducer( KafkaClient(KAFKA_HOST) )
# init kafka condumer 
consumer = KafkaConsumer( TPC_REQUEST,
                          group_id=KAFKA_GRP_ID,
                          bootstrap_servers=[KAFKA_HOST])
for message in consumer:
  if (DEBUG):
    # debug output
    print("%s:%d:%d: key=%s value=%s" % ( message.topic, 
                                          message.partition,
                                          message.offset,
                                          message.key,
                                          message.value))
  # send received message to processing
  result = processMessage(message.value)
  if (DEBUG):
    # debug output
    print result
  if result != None:
    # send result message back to kafka
    producer.send_messages( TPC_RESPONSE.encode("UTF8"), 
                            message.key,
                            result.encode("UTF8"))
   
