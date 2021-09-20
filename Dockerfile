FROM python:3.9.2

RUN apt update && apt install -y git vim tzdata
COPY . /graphing/
WORKDIR /graphing/
RUN pip install -r requirements.txt

ENV TZ Europe/Rome
EXPOSE 8088
ENTRYPOINT ["python", "./app.py"]

#  docker build --tag web_graph .
#  docker run -d -p 8088:8088 --name=bots_performance web_wine