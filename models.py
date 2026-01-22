"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class HealthResponse(BaseModel):
    status: str
    message: str
    version: str


class SurfSessionCreate(BaseModel):
    """Request model for creating a surf session"""
    # Required fields
    title: str = Field(..., min_length=1, max_length=200, description="Break name")
    description: str = Field(..., min_length=1, description="Session commentary")
    cost: float = Field(..., ge=0, le=100, description="Effort/difficulty score")
    estimated_return: float = Field(..., ge=0, le=100, description="Quality score")
    
    # Optional metadata
    date: Optional[date] = None
    time: Optional[str] = None
    zone: Optional[str] = None
    
    # Optional swell data
    swell_size_surfline: Optional[float] = None
    swell_size_seabreeze: Optional[float] = None
    swell_period: Optional[float] = None
    swell_direction: Optional[float] = None
    swell_score: Optional[float] = None
    swell_comments: Optional[str] = None
    
    # Optional wind data
    wind_bearing: Optional[str] = None
    wind_speed: Optional[float] = None
    wind_score: Optional[float] = None
    wind_comments: Optional[str] = None
    
    # Optional tide data
    tide_reading: Optional[float] = None
    tide_direction: Optional[str] = None
    tide_score: Optional[float] = None
    tide_comments: Optional[str] = None


class SurfSessionResponse(BaseModel):
    """Response model for surf session"""
    id: int
    title: str
    description: str
    total_score: float
    zone: Optional[str] = None
    created_at: str
    message: str = "Session recorded successfully!"


class SurfSessionList(BaseModel):
    """Response model for list of sessions"""
    sessions: list
    count: int
