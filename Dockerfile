FROM python:2-onbuild
ENTRYPOINT [ "python", "-u", "./server.py" ]

# Define Zookeeper host if different from Docker host machine
#ENV KAFKA_HOST=123.45.67.89:9092

