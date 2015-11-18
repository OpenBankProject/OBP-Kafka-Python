FROM python:2-onbuild
CMD [ "python", "./server.py" ]

# Define Zookeeper host if different from Docker host machine
ENV KAFKA_HOST=10.38.16.163:9092

