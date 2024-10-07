# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

ENV PORT=8080
EXPOSE $PORT

# Install system dependencies needed to build and install Poetry and the project
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* /app/

# Install dependencies defined in pyproject.toml using Poetry
RUN poetry install --with dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app

# Define the command to run the application using gunicorn
CMD poetry run gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 pypi_wayback:app
