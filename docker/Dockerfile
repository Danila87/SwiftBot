FROM python:3.11

LABEL authors="danila sergeev"

WORKDIR /SwiftBotApp

COPY src/requirements.txt .

RUN pip --no-cache-dir install -r requirements.txt

COPY src/. .

CMD ["python3", "main.py"]