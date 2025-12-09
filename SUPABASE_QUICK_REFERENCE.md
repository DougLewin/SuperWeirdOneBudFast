# Supabase Quick Reference

## SQL Scripts to Run in Supabase

### 1. Schema Setup (REQUIRED)
**File**: `database/01_schema.sql`  
**When**: First time setup  
**Where**: Supabase Dashboard → SQL Editor → New Query

Creates:
- `profiles` table
- `records` table  
- `communities` table
- `community_members` table
- All indexes
- RLS policies
- Triggers

### 2. Sample Data (OPTIONAL)
**File**: `database/02_seed.sql`  
**When**: Testing only  
**Note**: Uncomment INSERT statements and update UUIDs first

## Secrets Configuration

**File**: `.streamlit/secrets.toml` (create this file)

```toml
SUPABASE_URL = "https://yourproject.supabase.co"
SUPABASE_KEY = "eyJhbGc...your-anon-key"
```

**Get these from**: Supabase Dashboard → Settings → API

## Key Commands

### Install Dependencies
```powershell
pip install supabase==2.10.0
# or
pip install -r requirements.txt
```

### Run the App
```powershell
# New Supabase version
streamlit run superweirdonebud_supabase.py

# Original S3 version (for comparison)
streamlit run superweirdonebud.py
```

## User Flow

1. **First Time User**
   - App loads → Shows Sign Up / Sign In screen
   - User creates account → Receives verification email
   - User clicks verification link
   - User signs in → Sees main app

2. **Returning User**
   - App loads → Shows Sign Up / Sign In screen
   - User enters credentials → Sees their data
   - User can create/view/edit their records
   - User signs out → Returns to login screen

## Common SQL Queries

### Check if tables exist
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

### View all users
```sql
SELECT id, email, created_at 
FROM auth.users;
```

### View all records (admin view - bypasses RLS)
```sql
SELECT id, user_id, date, break, zone, total_score, publicity
FROM public.records;
```

### Check RLS policies
```sql
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE schemaname = 'public';
```

### Manually create a profile (if trigger didn't work)
```sql
INSERT INTO public.profiles (id, email, full_name)
VALUES 
  ('user-uuid-here', 'email@example.com', 'Full Name');
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "relation does not exist" | Run `01_schema.sql` in SQL Editor |
| "Failed to connect to Supabase" | Check secrets.toml has correct URL and KEY |
| Can't sign up | Check email format, password length (6+ chars) |
| Can't sign in | Verify email with verification link first |
| No records showing | Check you're logged in, check RLS policies enabled |
| Records visible to wrong users | Verify RLS policies ran successfully |

## API Endpoints (for reference)

```python
# Auth
supabase.auth.sign_up({"email": "", "password": ""})
supabase.auth.sign_in_with_password({"email": "", "password": ""})
supabase.auth.sign_out()

# Database
supabase.table('records').select('*').execute()
supabase.table('records').insert({...}).execute()
supabase.table('records').update({...}).eq('id', record_id).execute()
supabase.table('records').delete().eq('id', record_id).execute()

# Filters
.eq('field', value)
.neq('field', value)
.gt('field', value)
.gte('field', value)
.lt('field', value)
.lte('field', value)
.in_('field', [values])
.order('field', desc=True)
.limit(10)
```

## Files Overview

| File | Purpose |
|------|---------|
| `database/01_schema.sql` | Database schema (run in Supabase) |
| `database/02_seed.sql` | Sample data (optional) |
| `database/README.md` | Database setup guide |
| `superweirdonebud_supabase.py` | New app with auth |
| `superweirdonebud.py` | Original S3 app (keep for now) |
| `SUPABASE_MIGRATION_GUIDE.md` | Full migration steps |
| `SUPABASE_SETUP_SUMMARY.md` | What was delivered |
| `requirements.txt` | Updated with supabase |
| `.streamlit/secrets.toml.template` | Template for secrets |

## Security Checklist

- [ ] Never commit `.streamlit/secrets.toml` to git
- [ ] Use strong password for Supabase database
- [ ] Enable email verification (default on)
- [ ] RLS policies enabled on all tables
- [ ] Use `anon` key in client (not `service_role` key)
- [ ] Keep database password secure
- [ ] Enable 2FA on Supabase account (recommended)

## Testing Checklist

- [ ] Can create new user account
- [ ] Receive verification email
- [ ] Can sign in after verification
- [ ] Can create new surf session record
- [ ] Record appears in list after save
- [ ] Sign out and sign back in - data persists
- [ ] Create second user - each sees only their own data
- [ ] Edit record works
- [ ] Delete record works
- [ ] Public records visible to others (when implemented)

## Quick Links

- **Supabase Dashboard**: https://app.supabase.com
- **Your Project**: https://app.supabase.com/project/YOUR_PROJECT_ID
- **SQL Editor**: Dashboard → SQL Editor
- **Table Editor**: Dashboard → Table Editor → records
- **Auth Users**: Dashboard → Authentication → Users
- **API Settings**: Dashboard → Settings → API
- **Logs**: Dashboard → Logs → Postgres Logs

## Column Mappings (Database ↔ App)

| Database Column | App Column |
|----------------|------------|
| `surfline_primary_swell_size_m` | `Surfline Primary Swell Size (m)` |
| `seabreeze_swell_m` | `Seabreeze Swell (m)` |
| `swell_period_s` | `Swell Period (s)` |
| `wind_speed_kn` | `Wind Speed (kn)` |
| `tide_reading_m` | `Tide Reading (m)` |
| `total_score` | `TOTAL SCORE` |

*Conversion handled automatically in `superweirdonebud_supabase.py`*
