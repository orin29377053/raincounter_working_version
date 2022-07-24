FROM python:3.9

ENV TZ=Asia/Taipei \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y
RUN apt-get install -y cron
RUN apt-get install -y vim
RUN cron start

RUN apt update \
    && apt install -y tzdata \
    && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN date -R

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# COPY setCrontab.py ./
# RUN python3 /app/setCrontab.py