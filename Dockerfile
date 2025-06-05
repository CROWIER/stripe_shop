FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY pyproject.toml poetry.lock* ./

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

WORKDIR /code/src

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]