FROM python:3.10

WORKDIR /products

RUN pip install --upgrade pip

COPY requirements.txt /products

RUN pip install -r requirements.txt

COPY . .