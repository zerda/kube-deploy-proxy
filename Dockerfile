FROM alpine:3.6

RUN apk add --no-cache \
        uwsgi \
        uwsgi-python3 \
        python3

ENV HOME /webapp
WORKDIR /webapp
EXPOSE 80

ADD requirements.txt /webapp
RUN pip3 install --no-cache-dir -r requirements.txt
ADD . /webapp

ENTRYPOINT ["uwsgi", "--master", \
                     "--workers", "4", \
                     "--http-socket", "0.0.0.0:80", \
                     "--plugins", "python3", \
                     "--wsgi", "app:app"]