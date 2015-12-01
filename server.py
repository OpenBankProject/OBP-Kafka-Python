#!/usr/bin/python

import time
import re
import site
import obp
import os
import socket
import struct
import logging 

try:
  from kafka import KeyedProducer, KafkaConsumer, KafkaClient
except ImportError:
  pass
  # Use included module
  site.addsitedir('lib/')
  from kafka import KeyedProducer, KafkaConsumer, KafkaClient


# Define globals
TPC_RESPONSE = "Response"
TPC_REQUEST  = "Request"
KAFKA_GRP_ID = "1"
#DEBUG        = False
DEBUG        = True

# Get default gateway from /proc and use it as host address of Zookeeper
def get_default_gateway_linux():
  # open /rpc/net/route for reading
  with open("/proc/net/route") as fh:
    # read line by line
    for line in fh:
      # split fields on space
      fields = line.strip().split()
      # disregard fields we do not need
      if fields[1] != '00000000' or not int(fields[3], 16) & 2:
        continue
      # covert read field to ipv4 format
      return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

# determine zookeeper host from environment or use gateway address
try:
  os.environ["KAFKA_HOST"]
except KeyError:
  pass
  os.environ["KAFKA_HOST"] = get_default_gateway_linux() + ":9092"

# Split message and extract function name and arguments
# then pass them to obp.py for further processing 
#
def processMessage(message):
  reqFunc = None 
  reqArgs = None 
  # regex match function name
  decoded = message.decode()
  rFnc = re.match("^(.*?):{", decoded)
  if rFnc != None:
    reqFunc = rFnc.group(1)
  # regex match function arguments
  rArg = re.findall("[{,]\"(.*?)\":\"(.*?)\"", decoded)
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

# init logger
logging.basicConfig(format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s', level=logging.ERROR)

# Main loop waits indefinitely for requests 
# then passes them to processMessage()
#
while (True):
  try:
    # get the kafka host
    kafka_host = os.environ["KAFKA_HOST"]
    if (DEBUG): 
      print("Connecting to " + kafka_host + "...")
    # init kafka producer
    producer = KeyedProducer( KafkaClient(kafka_host) )
    if (DEBUG): 
      if (producer):
        print("producer: OK")
    # init kafka condumer 
    consumer = KafkaConsumer( TPC_REQUEST,
                              group_id=KAFKA_GRP_ID,
                              bootstrap_servers=[kafka_host] )
    if (DEBUG): 
      if (consumer):
        print("consumer: OK")
    # wait for new message in queue 
    if (DEBUG): 
      print("Connected. Waiting for messages...")
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
        print(result)
        print("")
      if result != None:
        # send result message back to kafka
        producer.send_messages( TPC_RESPONSE.encode("UTF8"), 
                                message.key,
                                result.encode("UTF8"))
  except Exception as e: 
    pass 
    z = e 
    print ("Exception: %s" % z)
  # print disconnect message, sleep for a while, and try to reconnect
  print("Error: Kafka disconnected. Reconnecting...")
  time.sleep(10)

