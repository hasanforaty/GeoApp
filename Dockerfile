FROM python:3.9-alpine3.19
LABEL maintainer="https://hasanforaty.github.io/"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./GeoApp /app
WORKDIR /app
EXPOSE 8000
ARG DEV=false
RUN apk add --no-cache \
            --upgrade \
        postgresql-client \
        libpq \
        nginx\
    && apk add --no-cache \
               --upgrade \
               --virtual .build-deps \
        postgresql-dev \
        zlib-dev jpeg-dev \
        alpine-sdk \
    && apk add --no-cache \
               --upgrade \
        geos \
        proj \
        gdal \
        gdal-dev \
        binutils \
    && ln -s /usr/lib/libproj.so.15 /usr/lib/libproj.so \
    && ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so

RUN python -m venv /env && \
    /env/bin/pip install --upgrade pip && \
#    apk add --update --no-cache postgresql-client && \
#    apk add --update --no-cache --virtual .tmp-build-deps \
#        build-base postgresql-dev musl-dev && \
    /env/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = 'true' ] ; \
        then /env/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
#    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/env/bin:$PATH"
USER django-user


