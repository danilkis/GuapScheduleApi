## base image
FROM arm64v8/python:3.11-slim-buster

## install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get install -y libpq-dev && \
    apt-get install -y openssl && \
    apt-get clean


## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## set working directory
WORKDIR /usr/src/app

## add user
RUN addgroup --system user && adduser --system --no-create-home --group user
RUN chown -R user:user /usr/src/app && chmod -R 755 /usr/src/app

## add and install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

## switch to non-root user
USER user

## add app
COPY . /usr/src/app

## run server
CMD python -m uvicorn main:app --reload --host 0.0.0.0 --port 1010
