FROM python:3.12.0b3-bullseye

RUN apk update \
    && apk add --no-cache mariadb-connector-c-dev \
                        build-base \
                        linux-headers \
                        mariadb-dev \
                        gcc \
                        musl-dev \
                        python3-dev \
                        pkgconfig

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]