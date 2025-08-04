FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add python-dotenv if not in requirements.txt
RUN pip install --no-cache-dir python-dotenv

# Copy project files
COPY . .

# Set permissions for entrypoint script
RUN chmod +x ./backend/run.py

# Expose port
EXPOSE 8026

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8026/health || exit 1

# Run the application
CMD ["python", "./backend/run.py"]
