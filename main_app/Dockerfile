FROM python:3.11-slim

WORKDIR /main_app

COPY . . 

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 wsgi:app