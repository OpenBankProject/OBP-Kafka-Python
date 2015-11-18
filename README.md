# OBP-Kafka-Python

Listens to Kafka queue and responds to requests from OBP-API



# Requirements

- Python (http://python.org)
- kafka-python (pip install kafka-python)
- Docker (http://docker.com)



# Running from command line

Note: replace hostname_or_ip with address

$ export KAFKA_HOST=hostname_or_ip:9092
$ python server.py


# Runnig from Docker

Edit Dockerfile and set KAFKA_HOST
run ./build_and_install_container.sh

