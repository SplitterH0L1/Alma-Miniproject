FROM python:3.9-slim-buster

EXPOSE 5000/tcp

ENV VIRTUAL_ENV=/opt/venv

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY alma .

RUN pip install -r requirements.txt

CMD [ "flask", "run" ]
