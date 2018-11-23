FROM python:3.6

RUN apt-get update
RUN apt-get install python python-pip -y
RUN mkdir /opt/app
COPY manage.py /opt/app/
COPY requirements.txt /opt/app/
RUN pip install -r /opt/app/requirements.txt

COPY docker-entrypoint.sh /

EXPOSE 5000
ENTRYPOINT "/docker-entrypoint.sh"
