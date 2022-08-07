FROM bitnami/nginx:1.23.1-debian-11-r6

WORKDIR /app

COPY ./app/ .

COPY ./app/nginx.conf /etc/nginx/nginx.conf
