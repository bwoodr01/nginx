FROM bitnami/nginx:1.23.1-debian-11-r6

WORKDIR /app

COPY app/static/ /opt/bitnami/nginx/html/static/

COPY app/nginx.conf /opt/bitnami/nginx/conf/bitnami/static.conf
