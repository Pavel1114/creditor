FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && apk add postgresql-client \
  && apk add git

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/base.txt && pip install -r /requirements/local.txt

COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/django/start_django_devserver.sh /start_django_devserver.sh
RUN chmod +x /start_django_devserver.sh

COPY ./compose/django/start_celeryworker.sh /start_celeryworker.sh
RUN chmod +x /start_celeryworker.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
