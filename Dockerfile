# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed wheels from the builder stage
COPY --from=builder /app/wheels /wheels

# Install dependencies from wheels
RUN pip install --no-cache /wheels/*

# Copy the application source code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using Gunicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--conf", "gunicorn_conf.py", "src.main:app"]
