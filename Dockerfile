FROM python:3.12 AS fastapi-app
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["python", "main.py"]