FROM python:3.11-slim

WORKDIR /src

# install dependencies
RUN pip install --no-cache-dir poetry

# copy poetry files
COPY pyproject.toml poetry.lock ./

COPY /data/Interns_2025_SWIFT_CODES.xlsx ./

RUN poetry config virtualenvs.create true \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

# TODO here testing in the future