FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8081"]