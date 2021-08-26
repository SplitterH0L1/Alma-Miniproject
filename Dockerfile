FROM python:3.9-alpine

RUN apk update && apk add --no-cache nano

EXPOSE 5000/tcp

COPY alma /usr/src/alma

WORKDIR /usr/src/

RUN pip install virtualenv \
    && python3 -m venv venv \
    && . venv/bin/activate

RUN export FLASK_APP=alma.py

WORKDIR /usr/src/alma

RUN pip install -r requirements.txt

CMD [ "flask", "run" ]
