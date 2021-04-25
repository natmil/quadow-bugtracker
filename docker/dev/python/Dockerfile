FROM python:3.9.2-slim-buster
MAINTAINER logurbate@localhost

COPY ./docker/dev/python/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /quadow

COPY ./quadow/requirements /quadow/requirements

RUN pip install --no-cache-dir -r requirements/dev.txt

COPY ./quadow /quadow

ENTRYPOINT ["/entrypoint.sh"]