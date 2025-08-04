from app.api.api import api_router
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import logging
from app.config import settings
from app.api.discovery import discovery_data

# Configure logging
log_level = getattr(logging, settings.log.level.upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load Swagger specification
def load_swagger_spec():
    """Load the Swagger/OpenAPI specification from swagger.json"""
    swagger_path = os.path.join(os.path.dirname(__file__), "../../swagger.json")
    if os.path.exists(swagger_path):
        with open(swagger_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# Load custom OpenAPI spec
custom_openapi = load_swagger_spec()

# FastAPI application with enhanced configuration
app = FastAPI(
    title="AI Assist Backend API",
    description="""
    A dynamic FastAPI backend that serves AI application data from JSON configuration files.
    
    ## Features
    
    * **Dynamic API Generation**: Endpoints dynamically load data from JSON files
    * **Simple Discovery API**: Access complete application configuration data with a single endpoint
    * **Multi-Application Support**: Supports both Appfoundry and ModelGarden applications
    * **No Hardcoded Values**: All data comes from configuration files
    * **UTF-8 Support**: Full Unicode support for international characters and emojis
    
    ## Available Applications
    
    * **Appfoundry**: AI-powered application deployment platform with blueprint management
    * **ModelGarden**: AI Model Management and Deployment Platform
    
    ## Data Sources
    
    The API reads data from the following JSON files:
    1. `home.json`: Main application routes and configuration
    2. `appfoundry.json`: Complete Appfoundry application configuration
    3. `modelgarden.json`: Complete ModelGarden application configuration
    """,
    version="1.0.0",
    contact={
        "name": "AI Assist Team",
        "url": "https://github.com/your-org/ai-assist",
        "email": "support@ai-assist.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    servers=[
        {
            "url": "http://localhost:8026",
            "description": "Development server"
        },
        {
            "url": "https://api.ai-assist.com", 
            "description": "Production server"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Explicitly allow all origins
    allow_credentials=False,  # Cannot use wildcard origin with credentials
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Override OpenAPI schema with custom specification if available
if custom_openapi:
    def custom_openapi_schema():
        return custom_openapi
    app.openapi = custom_openapi_schema

# Include API router
app.include_router(api_router)

# Redirect root to documentation
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Health check endpoint
@app.get("/health", tags=["health"], summary="Health Check")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "AI Assist Backend is running"}

# API info endpoint
@app.get("/info", tags=["info"], summary="API Information")
async def api_info():
    """Get information about the API and loaded data"""
    try:
        # Use discovery_data from the discovery module
        info = {
            "api": {
                "title": "AI Assist Backend API",
                "version": "1.0.0",
                "description": "Dynamic API serving AI application data"
            },
            "data_sources": list(discovery_data.keys()) if discovery_data else [],
            "status": "operational"
        }
        
        # Add application statistics
        info["applications"] = {}
        
        # Add home info if available
        if 'home' in discovery_data:
            home_data = discovery_data['home']
            info["home"] = {
                "application_count": len(home_data.get("application", {})),
                "routes_available": bool(home_data.get("application"))
            }
        
        # Add appfoundry info if available
        if 'appfoundry' in discovery_data:
            appfoundry = discovery_data['appfoundry'].get('appfoundry', {})
            info["applications"]["appfoundry"] = {
                "name": appfoundry.get("name"),
                "version": appfoundry.get("version"),
                "pages_count": len(appfoundry.get("pages", [])),
                "blueprints_count": len(appfoundry.get("blueprints", []))
            }
        
        # Add modelgarden info if available
        if 'modelgarden' in discovery_data:
            modelgarden = discovery_data['modelgarden'].get('modelgarden', {})
            info["applications"]["modelgarden"] = {
                "name": modelgarden.get("name"),
                "version": modelgarden.get("version"),
                "pages_count": len(modelgarden.get("pages", [])),
                "providers_count": len(modelgarden.get("providers", []))
            }
        
        return info
        
    except Exception as e:
        return {
            "api": {
                "title": "AI Assist Backend API",
                "version": "1.0.0",
                "description": "Dynamic API serving AI application data"
            },
            "status": "operational",
            "data_sources": [],
            "error": f"Could not load data info: {str(e)}"
        }
