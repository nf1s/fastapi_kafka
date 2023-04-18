FROM python:3.10.5-slim-buster AS builder

ENV POETRY_VERSION=1.3.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"
WORKDIR /build

COPY poetry.lock pyproject.toml  ./

RUN pip install poetry

RUN poetry export \
    --without-hashes \
    -f requirements.txt \
    --output requirements.txt \
    --only main

RUN pip install --prefix /local --no-cache-dir pip && \
    pip install --prefix /local -I --no-cache-dir -r requirements.txt

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

FROM python:3.10.5-slim-buster
ENV PYTHONUNBUFFERED=1
RUN useradd -d /app --create-home app
COPY --from=builder /local/ /usr/local
COPY --from=builder /wait /app
COPY --chown=app:app . /app
USER app
WORKDIR /app
