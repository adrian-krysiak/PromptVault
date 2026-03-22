FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY . .

CMD python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    gunicorn config.wsgi:application --bind 0.0.0.0:8081 --workers 2 --timeout 120 --access-logfile - --error-logfile -