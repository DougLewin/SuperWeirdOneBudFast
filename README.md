# Super Weird One Bud API

FastAPI backend for Rottnest Island Surf Tracker
 
## Quick Start

```bash
# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your Supabase credentials

# Run
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs

## Files

- `main.py` - API routes and endpoints
- `models.py` - Pydantic validation models
- `db.py` - Database connection
- `requirements.txt` - Dependencies
- `.env` - Environment variables (create from .env.example)

## Environment Variables

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

## API Endpoints

- `GET /health` - Health check
- `POST /submit-idea` - Create surf session
- `GET /surf-sessions` - List sessions (filterable)
- `GET /surf-sessions/{id}` - Get session
- `DELETE /surf-sessions/{id}` - Delete session

## Supabase Setup

Run this SQL in your Supabase SQL editor:

```sql
CREATE TABLE surf_sessions (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date DATE,
    time TEXT,
    break TEXT,
    zone TEXT,
    total_score NUMERIC,
    surfline_primary_swell_size NUMERIC,
    seabreeze_swell_size NUMERIC,
    swell_period NUMERIC,
    swell_direction NUMERIC,
    swell_score NUMERIC,
    swell_comments TEXT,
    wind_bearing TEXT,
    wind_speed NUMERIC,
    wind_score NUMERIC,
    wind_comments TEXT,
    tide_reading NUMERIC,
    tide_direction TEXT,
    tide_score NUMERIC,
    tide_comments TEXT,
    full_commentary TEXT,
    cost NUMERIC,
    estimated_return NUMERIC
);

CREATE INDEX idx_surf_sessions_total_score ON surf_sessions(total_score DESC);
CREATE INDEX idx_surf_sessions_zone ON surf_sessions(zone);
CREATE INDEX idx_surf_sessions_break ON surf_sessions(break);

ALTER TABLE surf_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable all for all users" ON surf_sessions FOR ALL USING (true);
```

## Vercel Deployment

1. **Install Vercel CLI** (optional, for local testing): `npm i -g vercel`
2. **Push to GitHub**
3. **Import Project in Vercel Dashboard**
   - Connect your GitHub repository.
   - Framework Preset: **Other** (Override if necessary, but Vercel detects Python).
   - **Environment Variables**: Add `SUPABASE_URL` and `SUPABASE_KEY`.
4. **Deploy**

The `vercel.json` file handles the configuration, directing traffic to `main.py`.

## Tech Stack

- FastAPI
- Uvicorn
- Supabase
- Python 3.10+
