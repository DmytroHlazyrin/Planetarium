FROM python:3.10-alpine3.20
LABEL maintainer="dmytro.hlazyrin@gmail.com"
ENV PYTHONBUFFERED 1

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p /files/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user
RUN chown -R my_user /files/media/
RUN chown -R 755 /files/media

USER my_user
