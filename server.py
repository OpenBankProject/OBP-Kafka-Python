#!/usr/bin/python

import time
import re
import site
import obp
import os
import socket
import struct

try:
  from kafka import KeyedProducer, KafkaConsumer, KafkaClient
except ImportError:
  pass
  # Use included module
  site.addsitedir('lib/')
  from kafka import KeyedProducer, KafkaConsumer, KafkaClient

try:
  from kazoo.client import KazooClient
except ImportError:
  pass
  # Use included module
  site.addsitedir('lib/')
  from kazoo.client import KazooClient

try:
  from samsa.cluster import Cluster
except ImportError:
  pass
  # Use included module
  site.addsitedir('lib/')
  from samsa.cluster import Cluster


# Define globals
TPC_RESPONSE = "Response"
TPC_REQUEST  = "Request"
KAFKA_GRP_ID = "0"
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
  os.environ["ZOOKEEPER_HOST"]
except KeyError:
  pass
  os.environ["ZOOKEEPER_HOST"] = get_default_gateway_linux() + ":2181"

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
while (True):
  try:
    # get the zookeeper host
    zookeeper_host = os.environ["ZOOKEEPER_HOST"]
    # connect to zookeeper
    zookeeper = KazooClient(hosts=zookeeper_host)
    zookeeper.start()
    # connect to kafka cluster
    cluster = Cluster(zookeeper)
    print("fff")
    # set request and response topics
    reqTopic = cluster.topics.get(TPC_REQUEST)
    resTopic = cluster.topics.get(TPC_RESPONSE)
    # init kafka consumer 
    consumer = reqTopic.subscribe(KAFKA_GRP_ID)
    # wait for new message in queue 
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
      if result != None:
        # send result message back to kafka
        resTopic.publish(result.encode("UTF8"), message.key)
  except Exception as e: 
    pass 
    z = e 
    print z
  # print disconnect message, sleep for a while, and try to reconnect
  print("Error: Kafka disconnected. Reconnecting...")
  time.sleep(10)

