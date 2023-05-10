FROM python:3.10-slim

# install dependencies
COPY ./pyproject.toml ./pyproject.toml
RUN pip install poetry==1.4.2
RUN poetry install --no-root

# copy project
COPY ./src ./src

ENTRYPOINT poetry run bot