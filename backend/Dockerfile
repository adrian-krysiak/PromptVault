FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install django djangorestframework psycopg2-binary

CMD ["sh", "-c", "echo 'Backend service is running...' && sleep infinity"]