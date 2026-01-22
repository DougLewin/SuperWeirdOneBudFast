"""
FastAPI Backend - Super Weird One Bud Surf Tracker
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional

from models import HealthResponse, SurfSessionCreate, SurfSessionResponse, SurfSessionList
from db import get_db

# Initialize app
app = FastAPI(
    title="Super Weird One Bud API",
    description="Surf Conditions Tracker",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint for Railway"""
    return {
        "status": "online", 
        "message": "System operational",
        "version": "1.0.0"
    }


def calculate_score(cost: float, estimated_return: float, 
                    swell_score: Optional[float] = None,
                    wind_score: Optional[float] = None,
                    tide_score: Optional[float] = None) -> float:
    """Calculate total session score"""
    base = estimated_return - cost
    scores = [s for s in [swell_score, wind_score, tide_score] if s is not None]
    
    if scores:
        conditions = sum(scores) / len(scores)
        return round((conditions * 0.6) + (base * 0.4), 1)
    return round(base, 1)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hello World"}


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check for Railway"""
    return {"status": "healthy", "message": "API running", "version": "1.0.0"}


@app.post("/submit-idea", response_model=SurfSessionResponse, status_code=201)
async def create_session(session: SurfSessionCreate):
    """Create new surf session"""
    try:
        db = get_db()
        
        # Calculate score
        total = calculate_score(
            session.cost,
            session.estimated_return,
            session.swell_score,
            session.wind_score,
            session.tide_score
        )
        
        # Prepare data
        data = {
            "date": session.date.isoformat() if session.date else datetime.now().date().isoformat(),
            "time": session.time or datetime.now().strftime("%H:%M"),
            "break": session.title,
            "zone": session.zone,
            "total_score": total,
            "surfline_primary_swell_size": session.swell_size_surfline,
            "seabreeze_swell_size": session.swell_size_seabreeze,
            "swell_period": session.swell_period,
            "swell_direction": session.swell_direction,
            "swell_score": session.swell_score,
            "swell_comments": session.swell_comments,
            "wind_bearing": session.wind_bearing,
            "wind_speed": session.wind_speed,
            "wind_score": session.wind_score,
            "wind_comments": session.wind_comments,
            "tide_reading": session.tide_reading,
            "tide_direction": session.tide_direction,
            "tide_score": session.tide_score,
            "tide_comments": session.tide_comments,
            "full_commentary": session.description,
            "cost": session.cost,
            "estimated_return": session.estimated_return
        }
        
        # Insert
        result = db.table("surf_sessions").insert(data).execute()
        
        if not result.data:
            raise HTTPException(500, "Failed to create session")
        
        record = result.data[0]
        
        return SurfSessionResponse(
            id=record["id"],
            title=session.title,
            description=session.description,
            total_score=total,
            zone=session.zone,
            created_at=record.get("created_at", datetime.now().isoformat())
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.get("/surf-sessions", response_model=SurfSessionList)
async def get_sessions(
    zone: Optional[str] = None,
    break_name: Optional[str] = None,
    min_score: Optional[float] = None,
    limit: int = 50,
    offset: int = 0
):
    """Get surf sessions with optional filters"""
    try:
        db = get_db()
        query = db.table("surf_sessions").select("*")
        
        if zone:
            query = query.eq("zone", zone)
        if break_name:
            query = query.ilike("break", f"%{break_name}%")
        if min_score is not None:
            query = query.gte("total_score", min_score)
        
        query = query.order("total_score", desc=True).range(offset, offset + limit - 1)
        result = query.execute()
        
        return SurfSessionList(sessions=result.data, count=len(result.data))
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.get("/surf-sessions/{session_id}")
async def get_session(session_id: int):
    """Get single surf session"""
    try:
        db = get_db()
        result = db.table("surf_sessions").select("*").eq("id", session_id).execute()
        
        if not result.data:
            raise HTTPException(404, f"Session {session_id} not found")
        
        return result.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.delete("/surf-sessions/{session_id}", status_code=204)
async def delete_session(session_id: int):
    """Delete surf session"""
    try:
        db = get_db()
        result = db.table("surf_sessions").delete().eq("id", session_id).execute()
        
        if not result.data:
            raise HTTPException(404, f"Session {session_id} not found")
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    import os
    # Use the PORT environment variable if it exists, otherwise default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
