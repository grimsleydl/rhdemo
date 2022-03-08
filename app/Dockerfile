FROM python:3.10.2-slim-bullseye AS base
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

FROM base as poetry
RUN pip install poetry==1.1.12
COPY poetry.lock pyproject.toml /app/
RUN poetry export -o requirements.txt

FROM base as build
COPY --from=poetry /app/requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get -y --no-install-recommends install libmariadb3 libmariadb-dev build-essential
RUN python -m venv .venv && \
    .venv/bin/pip install 'wheel==0.37.1' && \
    .venv/bin/pip install -r /tmp/requirements.txt
FROM python:3.10.2-slim-bullseye AS runtime
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
ENV PATH=/app/.venv/bin:$PATH
COPY --from=build /app/.venv /app/.venv
COPY rhdemo_py/ /app/

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    libmariadb-dev-compat \
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -r user && \
    chown user /app

ENV TINI_VERSION="v0.19.0"
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

USER user

EXPOSE 5000

ENTRYPOINT ["/tini", "--"]

CMD ["python", "/app/app.py"]
