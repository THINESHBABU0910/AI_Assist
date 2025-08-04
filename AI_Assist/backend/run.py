#!/usr/bin/env python3
"""
Production entrypoint for the FastAPI application.
Uses Uvicorn server with proper configuration for production.
"""

import uvicorn
import logging
import os
from app.config import settings

if __name__ == "__main__":
    # Set up logging
    log_level = getattr(logging, settings.log.level.upper(), logging.INFO)
    
    # Print configuration for debugging
    print(f"Starting server with configuration:")
    print(f"Port: {settings.api.port} (from env: {os.getenv('API_PORT', 'not set')})")
    print(f"Host: {settings.api.host}")
    print(f"Workers: {settings.api.workers}")
    print(f"Debug mode: {settings.app.debug}")
    
    # Configure and start Uvicorn server
    uvicorn.run(
        "app.main:app",
        host=settings.api.host,
        port=settings.api.port,
        workers=settings.api.workers,
        log_level=settings.log.level.lower(),
        timeout_keep_alive=settings.api.timeout,
        reload=settings.app.debug,  # Only reload in debug mode
        access_log=True,
        proxy_headers=True,  # Trust proxy headers (important behind load balancers)
        forwarded_allow_ips="*",  # Allow forwarded IP headers from all sources
    )
