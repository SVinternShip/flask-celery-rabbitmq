FROM python:3.9.12

COPY . /app/
WORKDIR /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=celery_app
ENV FLASK_ENV=development

CMD [ "flask", "run", "--host=0.0.0.0" ]
