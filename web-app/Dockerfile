
FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 4000

ENV GOOGLE_APPLICATION_CREDENTIALS="sunny-resolver-406200-d6e8c0dfe225.json"

CMD ["python", "app.py"]