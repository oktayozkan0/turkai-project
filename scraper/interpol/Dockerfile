FROM ubuntu:focal

ADD crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN touch /var/log/cron.log


RUN apt-get update && apt-get install tzdata && apt-get -y install cron

RUN apt-get install -y python3 python3-pip
RUN apt-get clean
RUN pip3 install scrapy scrapyd pika

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

COPY . $APP_HOME/

CMD cron && tail -f /var/log/cron.log