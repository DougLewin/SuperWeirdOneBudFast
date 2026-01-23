from fastapi import APIRouter
from models import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "System operational",
        "version": "1.0.0"
    }
