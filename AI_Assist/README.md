# AI Assist Backend

A FastAPI-based backend service that provides dynamic APIs for managing AI applications and models. The system reads configuration from JSON/YAML files and serves paginated API endpoints for application data.

## Features

- **Dynamic API Generation**: All endpoints dynamically load data from JSON/YAML configuration files
- **Paginated Responses**: JSON:API compliant pagination for all list endpoints
- **Multi-Application Support**: Supports both Appfoundry and ModelGarden applications
- **No Hardcoded Values**: All data comes from configuration files, no fallback defaults
- **UTF-8 Support**: Full Unicode support for international characters and emojis
- **Docker Support**: Production-ready Docker and Docker Compose setup
- **Environment Configuration**: All settings configurable via .env file

## Quick Start with Docker

The easiest way to run the application in production mode is with Docker Compose:

```bash
# Clone the repository
git clone https://github.com/your-organization/AI_Assist.git
cd AI_Assist

# Start with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

The API will be available at http://localhost:8000

## Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/your-organization/AI_Assist.git
cd AI_Assist
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure the environment variables in .env file:
```bash
# Edit .env with your preferred settings
```

4. Run the application:
```bash
# For production mode:
python backend/run.py

# For development mode with auto-reload (bypasses the port in .env):
cd backend
uvicorn app.main:app --reload --port 8026

# To use the port from .env in development:
cd backend
python -c "from app.config import settings; import uvicorn; uvicorn.run('app.main:app', host=settings.api.host, port=settings.api.port, reload=True)"
```

## Project Structure

```
AI_Assist/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── pages.py          # Main API router
│   │   ├── files/
│   │   │   └── application.json  # Primary data source
│   │   ├── config.py            # Configuration handling
│   │   └── main.py              # FastAPI application entry point
│   └── run.py                   # Production entry point
├── Dockerfile                   # Docker build configuration
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
├── .env                         # Environment configuration
└── README.md                    # This file
```

## Configuration (.env)

The application uses a `.env` file for configuration. Here are the available settings:

```
# API Configuration
API_PORT=8000                 # Port for the API server
API_HOST=0.0.0.0              # Host to bind the API server
API_WORKERS=4                 # Number of worker processes
API_TIMEOUT=300               # Timeout in seconds

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3003"]  # Allowed origins
CORS_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]         # Allowed methods
CORS_HEADERS=["Content-Type", "Authorization", "X-API-KEY"]      # Allowed headers
CORS_CREDENTIALS=true                                            # Allow credentials

# Application Settings
DEBUG=false                   # Debug mode (don't use in production)
APP_NAME=AI_Assist           # Application name
APP_VERSION=1.0.0             # Application version
DATA_DIR=./backend/app/files  # Data directory for JSON/YAML files

# Logging
LOG_LEVEL=info               # Log level (debug, info, warning, error, critical)
LOG_FORMAT=json               # Log format (json or text)
```

## Docker Usage

### Building the Docker Image

```bash
docker build -t ai-assist:latest .
```

### Running with Docker

```bash
docker run -p 8000:8000 --env-file .env ai-assist:latest
```

### Running with Docker Compose

```bash
docker-compose up -d
```

## API Endpoints

### 1. List Pages

```
GET /api/v1/pages?page[number]=1&page[size]=50
```

Returns paginated list of all available pages from both Appfoundry and ModelGarden applications.

**Response Format:**

```json
{
  "links": {
    "self": "/api/v1/pages?page[number]=1&page[size]=50",
    "first": "/api/v1/pages?page[number]=1&page[size]=50",
    "prev": null,
    "next": "/api/v1/pages?page[number]=2&page[size]=50",
    "last": "/api/v1/pages?page[number]=3&page[size]=50"
  },
  "meta": {
    "page": {
      "number": 1,
      "size": 50,
      "total_pages": 3,
      "total_items": 125
    }
  },
  "data": [
    {
      "id": "appfoundry",
      "route": "/appfoundry",
      "title": "Appfoundry",
      "summary": "AI-powered application deployment platform"
    }
  ]
}
```

### 2. Page Details

```
GET /api/v1/pages/{id}
```

Returns detailed information about a specific page, including technology stack, endpoints, and features.

**Example:**

```
GET /api/v1/pages/appfoundry
```

### 3. Page Actions

```
GET /api/v1/pages/{id}/actions?page[number]=1&page[size]=20
```

Returns paginated list of available actions for a specific page.

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "AI Platform/AI_Assist"
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Verify Data Files

Ensure the following files exist in `backend/app/files/`:

- `application.json` (Primary data source)
- `application.yaml` (Backup data source)

### 5. Run the Server

```bash
# Development server
uvicorn app.main:app --reload 

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8026
```

### 6. Access the API

- **API Base URL**: `http://localhost:`

## Configuration

### Data Sources

The API reads data from two sources in order of priority:

1. `application.json` (Primary)
2. `application.yaml` (Backup)

### JSON Structure

The `application.json` file should contain:

```json
{
  "application": {
    "appfoundry": {
      "id": "appfoundry",
      "name": "Appfoundry",
      "version": "0.1.0",
      "description": "AI-powered application deployment platform",
      "route": "/appfoundry",
      "pages": [...],
      "blueprints": [...],
      "api_endpoints": {...},
      "technology_stack": [...]
    },
    "modalgarden": {
      "id": "modalgarden",
      "name": "ModelGarden",
      "version": "0.1.0",
      "description": "AI Model Management and Deployment Platform",
      "route": "/modalgarden",
      "pages": [...],
      "providers": [...],
      "capabilities": [...]
    }
  }
}
```

## Development

### Adding New Endpoints

1. Edit `backend/app/api/pages.py`
2. Add new router functions following the existing pattern
3. Ensure data comes from JSON/YAML files only
4. Test with the interactive documentation

### Debug Mode

The application includes debug logging that shows:

- Loaded data sources
- Application keys found
- Page and blueprint counts

### Error Handling

- **404 Not Found**: When requested page/resource doesn't exist
- **422 Validation Error**: When request parameters are invalid
- **500 Internal Server Error**: When data files are missing or corrupted

## Testing

### Manual Testing

1. Start the server: `uvicorn app.main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Test each endpoint using the interactive documentation

### API Testing with cURL

```bash
# List pages
curl "http://localhost:8000/api/v1/pages?page[number]=1&page[size]=10"

# Get page details
curl "http://localhost:8000/api/v1/pages/appfoundry"

# Get page actions
curl "http://localhost:8000/api/v1/pages/appfoundry/actions"
```

## Deployment

### Production Deployment

```bash
# Install production dependencies
pip install -r requirements.txt

# Run with Gunicorn (recommended)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Or with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Ensure all data comes from JSON/YAML files (no hardcoded values)
5. Commit changes: `git commit -am 'Add new feature'`
6. Push to branch: `git push origin feature/new-feature`
7. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the interactive API documentation at `/docs`
2. Verify your data files (`application.json`, `application.yaml`) are properly formatted
3. Check the debug logs for data loading issues
4. Create an issue in the repository

## Changelog

### v1.0.0

- Initial release with dynamic API generation
- Support for Appfoundry and ModelGarden applications
- JSON:API compliant pagination
- UTF-8 and Unicode support
- No hardcoded fallback values - all data from configuration files
