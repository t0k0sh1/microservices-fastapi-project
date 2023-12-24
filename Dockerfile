# build stage
FROM python:3.12-alpine
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo

RUN pip install --upgrade pip
RUN pip install poetry==1.7.0

COPY . /app

RUN poetry config virtualenvs.create true
RUN if [ -f pyproject.toml ]; then poetry install --no-root --no-dev; fi

ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0"]
