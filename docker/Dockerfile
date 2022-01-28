FROM python:3.9.0

RUN mkdir /py
COPY requirements.txt /py/

RUN apt update && \
    pip install --upgrade pip && \
    apt install -y \
      locales \
      wget && \
    locale-gen ja_JP.UTF-8 && \
    pip install -r /py/requirements.txt

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL=ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8
