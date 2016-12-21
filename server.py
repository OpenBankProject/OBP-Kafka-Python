#!/usr/bin/python

import time
import re
import site
import obp
import os
import socket
import struct
import logging
import json

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
      #split fields on space
      fields = line.strip().split()
      # disregard fields we do not need
      if fields[1] != '00000000' or not int(fields[3], 16) & 2:
        continue
      # covert read field to ipv4 format
      return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

def getFuncName(data):
  j = json.loads(data)["north"]
  return j

def getArguments(data):
  r = dict()
  args = json.loads(data)
  for item in args.items():
    k = item[0]
    v = item[1]
    if (k != "north"):
      r.update({k:v})
  return r

# Split message and extract function name and arguments
# then pass them to obp.py for further processing 
#
def processMessage(message):
  reqFunc = None 
  reqArgs = None 
  decoded = message.decode()
  # extract function name 
  reqFunc = getFuncName(decoded)
  print(reqFunc)
  # return error if empty
  if reqFunc == None:
    return '{"error":"empty request"}'
  # return error if function name if not alphanumeric 
  if not re.match("^[a-zA-Z0-9_-]*$", reqFunc):
    return '{"error":"llegal request"}'
  # check if function name exists in obp.py
  if (hasattr(obp, reqFunc)):
    # extract function arguments
    reqArgs = getArguments(decoded)
    print(reqArgs)
    # create dictionary if not empty
    if reqArgs != None:
      # execute function from obp.py and return result
      return getattr(obp, reqFunc)(reqArgs)
    return '{"error":"arguments missing"}'
  else:
    return '{"error":"unknown request"}'

# determine if running on localhost or in docker container
kafka_host = "localhost:9092"
try:
  os.environ["ADVERTISED_HOST"]
except KeyError:
  pass
else:
  kafka_host = os.environ["ADVERTISED_HOST"] + ":9092"

print("Connecting to " + kafka_host + "...")
# try connecting to Kafka until successful
disconnected = True
while (disconnected):
  try:
    status = KeyedProducer( KafkaClient(kafka_host) )
    disconnected = False 
  except Exception as e:
    pass 
    disconnected = True
    print("Waiting for " + kafka_host + " to become available...")
    time.sleep(3)

# send initial status messages
try:
  status.send_messages( TPC_REQUEST.encode("UTF8"), "status","check".encode("UTF8"))
  status.send_messages( TPC_RESPONSE.encode("UTF8"), "status","check".encode("UTF8"))
except Exception as e:
  pass 

print("Connected to " + kafka_host + ".")

# init logger
logging.basicConfig(format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s', level=logging.ERROR)

# Main loop waits indefinitely for requests 
# then passes them to processMessage()
#
while (True):
  try:
    # kafka producer
    producer = KeyedProducer( KafkaClient(kafka_host) )
    if (DEBUG): 
      if (producer):
        print("producer: OK")
    consumer = KafkaConsumer( TPC_REQUEST,
                              group_id=KAFKA_GRP_ID,
                              bootstrap_servers=[kafka_host] )
    if (DEBUG): 
      if (consumer):
        print("consumer: OK")
      else:
        print("consumer: ERROR")
    # wait for new message in queue 
    if (DEBUG): 
      print("Connected. Waiting for messages...")
    for message in consumer:
      start_time = time.time()
      if (DEBUG):
        # debug output
        print("%s:%d:%d: key=%s value=%s" % ( message.topic, 
                                              message.partition,
                                              message.offset,
                                              message.key,
                                              message.value))
      # skip processing of internal status messages
      if message.key == "status" and message.value.decode() == "check":
        next
      # send received message to processing
      result = processMessage(message.value)
      #time.sleep(1)
      if (DEBUG):
        # debug output
        print(result)
        print("")
      if result != None:
        # send result message back to kafka
        producer.send_messages( TPC_RESPONSE.encode("UTF8"), 
                                message.key,
                                result.encode("UTF8"))
      print("--- %s seconds ---" % (time.time() - start_time))
  except Exception as e: 
    pass 
    print ("Exception: %s" % e)
    time.sleep(1)
  # print disconnect message, sleep for a while, and try to reconnect
  print("Info: Kafka disconnected. Reconnecting...")
  time.sleep(1)

