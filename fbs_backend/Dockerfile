# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=7860

# Set working directory inside container
WORKDIR /app

# Install system dependencies (needed for compiling some python packages if necessary)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt /app/

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Create a non-root user and switch to it for security
RUN useradd -u 1000 -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the default port for Hugging Face Spaces
EXPOSE 7860

# Run migrations and start gunicorn server
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn fbs_backend.wsgi:application --bind 0.0.0.0:7860 --workers 2 --timeout 120"]
