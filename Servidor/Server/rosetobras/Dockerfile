FROM python:3.5.9-alpine3.10

RUN pip install flask; pip install pika; pip install mysql-connector;

COPY main.py /

CMD ["python", "/main.py"]
