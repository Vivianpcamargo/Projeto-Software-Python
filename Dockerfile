FROM python:3.7-slim

RUN pip install flask
RUN pip install flask-mysql

RUN mkdir schemas
RUN mkdir static
RUN mkdir templates

COPY schemas/*  /schemas/
COPY static/*  /static/
COPY templates/*  /templates/

RUN chmod -R a+rwx schemas
RUN chmod -R a+rwx static
RUN chmod -R a+rwx templates

CMD ["python","app.py"]
