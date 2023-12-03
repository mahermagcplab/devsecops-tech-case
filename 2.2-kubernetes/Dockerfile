FROM python:3-alpine

RUN apk add nmap

WORKDIR /app

COPY scanner.py ./

CMD [ "python", "scanner.py", "10.244.0.0/24" ]
