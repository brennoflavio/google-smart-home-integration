FROM python:3.12

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml

RUN pip install poetry
RUN pip install poetry-plugin-export

RUN poetry export -f requirements.txt --output requirements.txt

RUN pip install -r requirements.txt

COPY ./src .
