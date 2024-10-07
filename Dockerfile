# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install any required system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install pypi-wayback using pip
RUN pip install --no-cache-dir pypi-wayback

# Define the command to run pypi-wayback using python -m on the port
CMD gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 pypi_wayback:app