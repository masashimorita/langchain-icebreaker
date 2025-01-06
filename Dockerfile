FROM python:3.10

RUN apt-get -y update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_IN_PROJECT 1

WORKDIR /app

RUN pip install poetry

COPY .venv ./

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

# Set the entrypoint to use poetry
ENTRYPOINT ["poetry", "run"]

# Expose the application port
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

CMD ["python", "app.py"]
