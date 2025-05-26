FROM python:latest

RUN pip install --no-cache-dir poetry

WORKDIR /code

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main --no-root

COPY ./src ./src

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "src/core/logging.yaml"]