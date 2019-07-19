FROM python:3.6-buster

RUN apt-get update && apt-get upgrade -y

RUN pip3 install flask requests

COPY app.py /opt/app.py

COPY start /opt/start

COPY data /opt/data/

WORKDIR /opt

EXPOSE 9002

CMD ["./start"]
