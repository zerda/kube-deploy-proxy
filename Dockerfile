FROM alpine:3.7

RUN apk add --no-cache \
        py3-gunicorn \
        py3-greenlet \
        py3-gevent \
        python3

ENV HOME /webapp
WORKDIR /webapp
EXPOSE 80

ADD src/requirements.txt /webapp
RUN pip3 install --no-cache-dir -r requirements.txt
ADD src /webapp

ENTRYPOINT ["gunicorn", "-w", "4", "-k", "gevent", "-b", "0.0.0.0:80", "app:app"]