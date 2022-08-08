FROM bitnami/nginx:1.23.1-debian-11-r6

WORKDIR /app

USER root

RUN \
    apt update && \
    apt install -y telnet \
    dnsutils

COPY app/static/ /opt/bitnami/nginx/html/static/

COPY app/nginx.conf /opt/bitnami/nginx/conf/bitnami/static.conf

USER 1001