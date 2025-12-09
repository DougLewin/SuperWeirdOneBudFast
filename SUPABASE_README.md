# 🏄 Super Weird One Bud - Supabase Backend Setup

Complete refactoring of the surf tracking application from AWS S3 storage to Supabase PostgreSQL database with user authentication.

## 📋 Table of Contents

- [What's Included](#whats-included)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Architecture](#architecture)
- [Next Steps](#next-steps)

## 🎯 What's Included

### Database Schema (`database/`)
- **Complete PostgreSQL schema** with 4 tables:
  - `profiles` - User profiles (auto-created on signup)
  - `records` - Surf session tracking (all your CSV columns + user_id)
  - `communities` - Community groups (future feature)
  - `community_members` - Community membership (future feature)
- **Row Level Security (RLS)** - Users only see their own data
- **Automatic triggers** - Timestamps and profile creation
- **Sample data** - Optional test records

### Application Code
- **`superweirdonebud_supabase.py`** - New Supabase-powered app with:
  - Email/password authentication
  - Session management
  - User-scoped database queries
  - Privacy controls (Private/Public/Community)
  - CRUD operations for surf sessions

### Documentation
- **`SUPABASE_MIGRATION_GUIDE.md`** - Complete step-by-step migration instructions
- **`SUPABASE_SETUP_SUMMARY.md`** - Overview of what was delivered
- **`SUPABASE_QUICK_REFERENCE.md`** - Cheat sheet for common tasks
- **`database/README.md`** - Database-specific setup guide

### Configuration
- **Updated `requirements.txt`** - Added `supabase==2.10.0`
- **Updated `.streamlit/secrets.toml.template`** - Supabase credentials format

## ⚡ Quick Start

### 1. Create Supabase Project (2 minutes)

```
1. Go to https://supabase.com
2. Click "New Project"
3. Fill in: Name, Password, Region
4. Wait for provisioning
```

### 2. Run Database Migration (1 minute)

```
1. Open Supabase Dashboard → SQL Editor
2. Copy contents of database/01_schema.sql
3. Paste and Run
4. Verify green checkmarks
```

### 3. Configure Secrets (1 minute)

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://yourproject.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
```

Get these from: **Supabase Dashboard → Settings → API**

### 4. Install and Run (1 minute)

```powershell
# Install Supabase client
pip install supabase==2.10.0

# Run the app
streamlit run superweirdonebud_supabase.py
```

### 5. Create Your First User

```
1. Click "Sign Up" tab
2. Enter email and password
3. Check email for verification link
4. Click link to verify
5. Return to app and sign in
6. Start tracking surf sessions!
```

**Total setup time: ~5 minutes** ⚡

## 📚 Documentation

### For Setup & Migration
- **Start here**: `SUPABASE_MIGRATION_GUIDE.md`
  - Detailed step-by-step instructions
  - Troubleshooting guide
  - Data migration from S3
  - Deployment instructions

### For Reference
- **Quick answers**: `SUPABASE_QUICK_REFERENCE.md`
  - Common commands
  - SQL queries
  - API examples
  - Troubleshooting table

### For Understanding
- **What was built**: `SUPABASE_SETUP_SUMMARY.md`
  - Architecture overview
  - Security features
  - Implementation status
  - Next steps

### For Database
- **Database setup**: `database/README.md`
  - Schema explanation
  - RLS policies
  - Triggers and functions
  - Testing procedures

## 🏗️ Architecture

### Database Tables

```
auth.users (Supabase managed)
    ↓
profiles (your table)
    ↓
records (surf sessions)
    - user_id → profiles.id
    - community_id → communities.id (optional)
    - publicity: Private/Public/Community

communities
    ↓
community_members
    - user_id → profiles.id
    - community_id → communities.id
```

### Security Model

```
Row Level Security (RLS) Policies:

Private records → Only owner can see
Public records → Everyone can see
Community records → Community members can see

Users can:
✅ Create their own records
✅ Read their own records
✅ Update their own records
✅ Delete their own records
❌ Cannot access other users' private data
```

### Application Flow

```
User not logged in
    ↓
Login/Signup Screen
    ↓
Email Verification (signup only)
    ↓
Main Application
    - View own records
    - Create new sessions
    - Edit/delete records
    - Sign out
```

## 🔐 Security Features

- ✅ **Email/password authentication** via Supabase Auth
- ✅ **Email verification** required for signup
- ✅ **Row Level Security (RLS)** on all tables
- ✅ **Automatic password hashing** by Supabase
- ✅ **Session management** via `st.session_state`
- ✅ **User-scoped queries** enforced by RLS
- ✅ **Prepared for social features** (Public/Community records)

## 📊 Data Model

### Records Table Columns

Original CSV columns + new fields:

```python
# New fields
- id (UUID) - Unique record ID
- user_id (UUID) - Owner of record
- community_id (UUID) - Optional community
- publicity (TEXT) - Private/Public/Community

# All your existing columns
- date, time, break, zone, total_score
- Swell: surfline_primary_swell_size_m, seabreeze_swell_m, swell_period_s, etc.
- Wind: wind_bearing, wind_speed_kn, suitable_wind, etc.
- Tide: tide_reading_m, tide_direction, tide_suitable, etc.
- full_commentary
```

## 🚀 Next Steps

### Immediate (Do This First)
1. ✅ Follow `SUPABASE_MIGRATION_GUIDE.md`
2. ✅ Set up Supabase project
3. ✅ Run database migration
4. ✅ Test authentication
5. ✅ Create and save a test record

### Short Term (This Week)
1. Integrate full UI from original `superweirdonebud.py`
2. Add all input fields (swell, wind, tide wizards)
3. Implement edit/delete functionality
4. Add filtering and sorting
5. Test with multiple users

### Medium Term (This Month)
1. Migrate existing S3 data to Supabase
2. Deploy to Streamlit Cloud
3. Add publicity selector to record forms
4. Test public record viewing
5. Refine UI/UX based on testing

### Long Term (Future)
1. Implement community features
2. Add social features (likes, comments)
3. Create analytics dashboard
4. Add data export functionality
5. Mobile-responsive improvements

## 🔄 Migration from S3

If you have existing data in S3, you have options:

### Option 1: Fresh Start
- Use Supabase going forward
- Keep S3 data as archive
- **Recommended if**: Testing or few existing records

### Option 2: Migrate All Data
- Write script to import S3 CSV to Supabase
- See `SUPABASE_MIGRATION_GUIDE.md` for example script
- **Recommended if**: Lots of existing records to preserve

### Option 3: Hybrid Approach
- Important records → manually re-enter
- Rest → keep in S3 for reference
- **Recommended if**: Want to clean/validate data during migration

## 🆘 Troubleshooting

### Quick Fixes

| Problem | Solution |
|---------|----------|
| Can't connect | Check `secrets.toml` has correct credentials |
| Can't sign up | Password must be 6+ characters |
| Can't sign in | Verify email first (check spam folder) |
| No data showing | Ensure you're logged in, check RLS enabled |
| "Relation does not exist" | Run `01_schema.sql` in Supabase |

### Get Help

1. Check `SUPABASE_QUICK_REFERENCE.md` for common issues
2. Review `SUPABASE_MIGRATION_GUIDE.md` troubleshooting section
3. Check Supabase logs: Dashboard → Logs → Postgres Logs
4. Verify RLS policies: `database/README.md`

## 📦 Files Reference

```
📁 Project Root
│
├── 📄 superweirdonebud.py (original S3 version)
├── 📄 superweirdonebud_supabase.py (NEW - Supabase version)
├── 📄 requirements.txt (updated with supabase)
│
├── 📁 database/
│   ├── 📄 01_schema.sql (run this first in Supabase)
│   ├── 📄 02_seed.sql (optional test data)
│   └── 📄 README.md (database setup guide)
│
├── 📁 .streamlit/
│   ├── 📄 secrets.toml.template (updated with Supabase)
│   └── 📄 secrets.toml (YOU CREATE THIS - not in git)
│
└── 📁 Documentation (NEW)
    ├── 📄 SUPABASE_MIGRATION_GUIDE.md (start here!)
    ├── 📄 SUPABASE_SETUP_SUMMARY.md (what was built)
    ├── 📄 SUPABASE_QUICK_REFERENCE.md (cheat sheet)
    └── 📄 SUPABASE_README.md (this file)
```

## 🎓 Learning Resources

- **Supabase Docs**: https://supabase.com/docs
- **Supabase Auth**: https://supabase.com/docs/guides/auth
- **Python Client**: https://supabase.com/docs/reference/python
- **RLS Guide**: https://supabase.com/docs/guides/auth/row-level-security
- **Streamlit**: https://docs.streamlit.io

## ✨ Features Roadmap

### ✅ Implemented
- User authentication (signup/signin)
- Session management
- User profiles auto-creation
- Database CRUD operations
- RLS security policies
- Basic UI (create/view records)

### 🔨 To Integrate
- Full multi-page form wizard
- All input validation
- Edit/delete with confirmation
- Advanced filtering
- Sorting and pagination
- Original styling

### 🚀 Future Features
- Community creation and management
- Public record browsing
- Social features (likes, shares)
- Advanced analytics
- Data export/import
- Mobile app (via PWA)

## 🤝 Contributing

Future development priorities:
1. Complete UI integration
2. Community features
3. Analytics dashboard
4. Mobile optimization
5. Performance improvements

## 📄 License

[Your License Here]

---

**Ready to get started?** → Open `SUPABASE_MIGRATION_GUIDE.md` and follow the steps!

**Need quick answers?** → Check `SUPABASE_QUICK_REFERENCE.md`

**Want to understand the setup?** → Read `SUPABASE_SETUP_SUMMARY.md`
