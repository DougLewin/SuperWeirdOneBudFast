"""
Database configuration and connection
"""
import os
from functools import lru_cache
from supabase import create_client, Client


@lru_cache()
def get_db() -> Client:
    """Get Supabase client (cached singleton)"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment")
    
    return create_client(url, key)
