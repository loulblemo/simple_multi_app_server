FROM python:3.11-slim

WORKDIR /app1

COPY . . 

RUN pip install -r requirements.txt

CMD SCRIPT_NAME=/app1 gunicorn --bind 0.0.0.0:5000 wsgi:app