# pull official base image
FROM python:3.11.3-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
# install system dependencies
# RUN apt-get update && apt-get install -y netcat \
#     && pip install mysqlclient \
#     && apt-get install -y default-libmysqlclient-dev


RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadbclient-dev

RUN apt-get update && apt-get install -y netcat pkg-config default-libmysqlclient-dev \
    && pip install mysqlclient

# RUN pip install mysqlclient
# install dependencies

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
