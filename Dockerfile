FROM python:latest

COPY /app ./app
COPY /config ./config
COPY .env ./
COPY README.md ./
COPY requirements.txt ./
COPY run.py ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

EXPOSE 8080

CMD [ "flask", "run"]