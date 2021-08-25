FROM python:3.9-alpine

EXPOSE 5000/tcp

COPY alma /usr/src/myapp/

WORKDIR /usr/src/myapp/

RUN pip3 install -r requirements.txt

CMD [ "python3", "./alma.py" ]
