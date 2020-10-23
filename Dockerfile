FROM python:3.8-alpine

RUN adduser -D business_game

WORKDIR /home/business_game

COPY requirements.txt requirements.txt


RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY app app
COPY migrations migrations
COPY game.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP game.py

RUN chown -R business_game:business_game ./
USER business_game

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
