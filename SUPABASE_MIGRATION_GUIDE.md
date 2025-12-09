# Supabase Migration Guide

This guide will help you migrate your Super Weird One Bud application from AWS S3 to Supabase for both authentication and data storage.

## Overview of Changes

### What's New
- **User Authentication**: Sign up/sign in functionality with email and password
- **PostgreSQL Database**: Records stored in Supabase instead of S3 CSV
- **Multi-User Support**: Each user has their own private data
- **Privacy Controls**: Records can be Private, Public, or Community-shared
- **Row Level Security**: Database-level security ensuring users only see their data

### Files Created/Modified
- ✅ `requirements.txt` - Added `supabase==2.10.0` dependency
- ✅ `database/01_schema.sql` - Complete database schema with tables, RLS policies, triggers
- ✅ `database/02_seed.sql` - Optional sample data for testing
- ✅ `database/README.md` - Database setup instructions
- ✅ `superweirdonebud_supabase.py` - New Supabase-powered application
- ✅ `.streamlit/secrets.toml.template` - Updated with Supabase credentials

## Step-by-Step Migration

### Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com) and sign in (or create account)
2. Click **"New Project"**
3. Fill in:
   - **Name**: `super-weird-one-bud` (or your preferred name)
   - **Database Password**: Choose a strong password (save it!)
   - **Region**: Choose closest to your users (e.g., Sydney for Australia)
   - **Pricing Plan**: Free tier is fine for getting started
4. Click **"Create new project"** and wait 1-2 minutes for provisioning

### Step 2: Run Database Migration

1. In your Supabase dashboard, click **"SQL Editor"** in the left sidebar
2. Click **"New Query"**
3. Open `database/01_schema.sql` and copy all contents
4. Paste into the Supabase SQL Editor
5. Click **"Run"** (or press `Ctrl+Enter`)
6. Verify all commands succeeded (green checkmarks)

### Step 3: Get Your Supabase Credentials

1. In Supabase dashboard, click **Settings** (gear icon) → **API**
2. Find and copy:
   - **Project URL** (e.g., `https://abcdefghijk.supabase.co`)
   - **anon public** key (long string starting with `eyJ...`)
3. Keep these safe - you'll need them in the next step

### Step 4: Configure Local Secrets

Create a file `.streamlit/secrets.toml` (without `.template`) in your project root:

```toml
SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

Replace with your actual values from Step 3.

**⚠️ Important**: Never commit `secrets.toml` to git! It's already in `.gitignore`.

### Step 5: Install Dependencies

```powershell
# Activate your virtual environment first
.\superweirdonebud_venv\Scripts\Activate.ps1

# Install new dependency
pip install supabase==2.10.0

# Or reinstall all requirements
pip install -r requirements.txt
```

### Step 6: Test the New Application

```powershell
# Run the Supabase version
streamlit run superweirdonebud_supabase.py
```

The app will open in your browser. You should see:
- Login/Signup screen instead of immediate data access
- Ability to create an account with email/password
- After login, a simplified surf tracking interface

### Step 7: Create Your First User

1. Click the **"Sign Up"** tab
2. Enter:
   - **Full Name**: (optional)
   - **Email**: Your email address
   - **Password**: At least 6 characters
   - **Confirm Password**: Same password
3. Click **"Sign Up"**
4. Check your email for verification link (check spam folder!)
5. Click verification link
6. Return to app and sign in with your credentials

### Step 8: Verify Everything Works

1. After signing in, you should see the main application
2. Click **"Create New Session"**
3. Fill in a test surf session
4. Click **"Save Session"**
5. Verify it appears in your session list
6. Sign out and sign back in - your data should persist

## Optional: Migrate Existing Data from S3

If you have existing data in S3 that you want to migrate to Supabase:

### Option A: Manual Migration Script (Recommended)

Create a file `migrate_s3_to_supabase.py`:

```python
import pandas as pd
import boto3
from supabase import create_client
import streamlit as st

# Load your secrets
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

# Load from S3
s3 = boto3.client('s3')
obj = s3.get_object(Bucket='superweirdonebud', Key='Rotto_Tracker.csv')
df = pd.read_csv(obj['Body'])

# You'll need to sign in first to get a user_id
user_email = "your-email@example.com"
user_password = "your-password"

response = supabase.auth.sign_in_with_password({
    "email": user_email,
    "password": user_password
})

user_id = response.user.id

# Convert and insert each record
for idx, row in df.iterrows():
    record = {
        'user_id': user_id,
        'publicity': 'Private',  # Make all imported records private
        'date': str(row['Date']),
        'time': str(row.get('Time', '08:00:00')),
        'break': row.get('Break'),
        'zone': row.get('Zone'),
        # ... map all other columns
    }
    
    supabase.table('records').insert(record).execute()
    print(f"Migrated record {idx + 1}/{len(df)}")

print("Migration complete!")
```

### Option B: CSV Import via Supabase Dashboard

1. Export your S3 data to a local CSV
2. In Supabase, go to **Table Editor** → **records**
3. Click **Import data from CSV**
4. **Note**: You'll need to manually add `user_id` column values first

## Deploying to Streamlit Cloud

1. Push your code to GitHub (make sure `secrets.toml` is NOT committed)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"**
4. Select your repository and `superweirdonebud_supabase.py`
5. Click **"Advanced settings"** → **"Secrets"**
6. Paste your secrets in TOML format:
   ```toml
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-anon-key-here"
   ```
7. Click **"Deploy"**

## Troubleshooting

### "Failed to connect to Supabase"
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct in secrets.toml
- Check your internet connection
- Ensure Supabase project is active (not paused)

### "Sign up failed: User already registered"
- This email is already registered
- Use "Sign In" instead or use a different email

### "Sign in failed: Invalid login credentials"
- Check email and password are correct
- Ensure you verified your email (check inbox/spam)
- Try password reset if needed

### Records not appearing after saving
- Check browser console for errors (F12)
- Verify you're logged in (check sidebar for email)
- Check Supabase Table Editor to see if record was inserted
- Verify RLS policies are enabled (run `01_schema.sql` again if unsure)

### Database query errors
- Ensure `01_schema.sql` ran completely without errors
- Check Supabase logs: Dashboard → Logs → Postgres Logs
- Verify table names are lowercase: `records`, `profiles`, etc.

## Security Notes

✅ **Built-in Security Features:**
- Row Level Security (RLS) enabled on all tables
- Users can only access their own data
- Email verification required for signup
- Secure password hashing by Supabase Auth
- API keys are "anon" keys - safe for client-side use

⚠️ **Best Practices:**
- Never commit `secrets.toml` to version control
- Use strong passwords for your Supabase database
- Enable 2FA on your Supabase account
- Regularly review access logs in Supabase dashboard
- Consider enabling Captcha for signup (Supabase settings)

## Next Steps

After successful migration:

1. **Test thoroughly** with multiple users
2. **Implement the full UI** by integrating the original `superweirdonebud.py` features into the new auth-protected version
3. **Add Community features** when ready (tables already exist in schema)
4. **Consider additional features**:
   - Password reset functionality
   - Profile customization
   - Data export
   - Advanced filtering
   - Social features (if using Public/Community records)

## Support Resources

- **Supabase Docs**: https://supabase.com/docs
- **Supabase Auth Guide**: https://supabase.com/docs/guides/auth
- **Python Client Docs**: https://supabase.com/docs/reference/python/introduction
- **RLS Guide**: https://supabase.com/docs/guides/auth/row-level-security

## Rolling Back (If Needed)

If you need to revert to the S3 version:

1. Stop the Supabase app
2. Run the original: `streamlit run superweirdonebud.py`
3. Your S3 data remains unchanged
4. You can keep both versions and choose which to use

---

**Questions or issues?** Check the troubleshooting section or review the database setup in `database/README.md`.
