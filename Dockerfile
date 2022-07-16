FROM python:3.9.12

WORKDIR /app/
COPY . /app/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt