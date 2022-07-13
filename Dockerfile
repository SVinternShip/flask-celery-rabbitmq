FROM python:3.9.12

COPY . /app/
WORKDIR /app/

RUN apt-get update
RUN pip3 install opencv-python-headless
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV FLASK_APP=celery_app
ENV FLASK_ENV=development

CMD [ "flask", "run", "--host=0.0.0.0" ]
