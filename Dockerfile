FROM python:2-onbuild
ENTRYPOINT [ "python", "-u", "./server.py" ]

