from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
import json
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Use the data directory from settings
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../files'))

# Dictionary to store loaded JSON data
discovery_data = {}

def load_discovery_files():
    discovery_files = ['home.json', 'appfoundry.json', 'modelgarden.json']
    for file_name in discovery_files:
        file_path = os.path.join(DATA_DIR, file_name)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    discovery_data[file_name.replace('.json', '')] = json.load(f)
                    logger.info(f"Successfully loaded {file_name}")
            except Exception as e:
                logger.error(f"Error loading {file_name}: {str(e)}")

# Load all discovery files when module is imported
load_discovery_files()

@router.get("/api/v1/get_pages/{id}", tags=["discovery"])
def get_discovery(id: str = Path(...)):
    # Check if the requested ID exists in our loaded data
    if id in discovery_data:
        return JSONResponse(discovery_data[id])
    
    return JSONResponse({"detail": f"Discovery '{id}' not found"}, status_code=404)
