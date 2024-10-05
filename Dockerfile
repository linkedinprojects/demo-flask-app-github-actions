FROM python:3.6

RUN pip install flask

COPY . /opt/

EXPOSE 80

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]
