FROM python:3.10

RUN apt-get -y update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install poetry

# COPY pyproject.toml poetry.lock ./

# RUN poetry install --no-root

COPY . .

# Expose the application port
EXPOSE 8000

# Set the entrypoint to use poetry
ENTRYPOINT ["poetry", "run"]
