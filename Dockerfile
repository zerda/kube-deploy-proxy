FROM alpine:3.9

RUN apk add --no-cache \
        py3-gunicorn \
        py3-greenlet \
        py3-gevent \
        python3

ENV HOME /app
WORKDIR /app
EXPOSE 80

ADD src/requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt
ADD src /app

ENTRYPOINT ["gunicorn", "-k", "gevent", "-b", "0.0.0.0:80", "proxy:app"]