FROM python:3.11-slim

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y postgresql-client

RUN chmod a+x docker/*.sh
