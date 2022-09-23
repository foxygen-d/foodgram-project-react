FROM python:3.7-slim 

WORKDIR /app 

COPY requirements.txt .
RUN apk update && apk add  --no-cache --virtual build-dependencies libc-dev build-base
RUN pip3 install -r requirements.txt --no-cache-dir 

COPY ./ /

WORKDIR /

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]