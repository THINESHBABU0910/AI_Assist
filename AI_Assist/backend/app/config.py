import os
import json
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent.absolute()


class CORSSettings(BaseModel):
    """CORS configuration settings."""
    origins: List[str]
    methods: List[str]
    headers: List[str]
    credentials: bool = True


class APISettings(BaseModel):
    """API configuration settings."""
    port: int
    host: str
    workers: int
    timeout: int


class AppSettings(BaseModel):
    """Application configuration settings."""
    debug: bool
    name: str
    version: str
    data_dir: str


class LogSettings(BaseModel):
    """Logging configuration settings."""
    level: str
    format: str


class Settings(BaseModel):
    """Main configuration settings."""
    cors: CORSSettings
    api: APISettings
    app: AppSettings
    log: LogSettings


def get_settings() -> Settings:
    """Get application settings from environment variables."""
    
    # Helper to parse JSON-like strings from environment variables
    def parse_json_env(env_var: str, default):
        value = os.getenv(env_var)
        if not value:
            return default
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return default
    
    # Parse CORS settings
    cors_origins = parse_json_env("CORS_ORIGINS", ["*"])  # Allow all origins for development
    cors_methods = parse_json_env("CORS_METHODS", ["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    cors_headers = parse_json_env("CORS_HEADERS", ["Content-Type", "Authorization", "X-API-KEY"])
    cors_credentials = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"
    
    # Parse API settings
    api_port = int(os.getenv("API_PORT", "8000"))
    api_host = os.getenv("API_HOST", "0.0.0.0")
    api_workers = int(os.getenv("API_WORKERS", "4"))
    api_timeout = int(os.getenv("API_TIMEOUT", "300"))

    # Parse application settings
    debug = os.getenv("DEBUG", "false").lower() == "true"
    app_name = os.getenv("APP_NAME", "AI_Assist")
    app_version = os.getenv("APP_VERSION", "1.0.0")
    data_dir = os.getenv("DATA_DIR", "./backend/app/files")
    
    # Parse log settings
    log_level = os.getenv("LOG_LEVEL", "info")
    log_format = os.getenv("LOG_FORMAT", "json")
    
    return Settings(
        cors=CORSSettings(
            origins=cors_origins,
            methods=cors_methods,
            headers=cors_headers,
            credentials=cors_credentials,
        ),
        api=APISettings(
            port=api_port,
            host=api_host,
            workers=api_workers,
            timeout=api_timeout,
        ),
        app=AppSettings(
            debug=debug,
            name=app_name,
            version=app_version,
            data_dir=data_dir,
        ),
        log=LogSettings(
            level=log_level,
            format=log_format,
        ),
    )


# Instantiate settings object
settings = get_settings()
