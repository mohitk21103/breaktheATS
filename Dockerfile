FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y gcc && apt-get clean

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


# Copy entire project
COPY . .

# Expose port
EXPOSE 8000

# Start app (assuming your Flask app is in main.py and app is named `app`)
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "main:app"]
