# Supabase Database Setup

This folder contains SQL migration scripts for setting up the Supabase PostgreSQL backend for the Super Weird One Bud surf tracking application.

## Files

- **01_schema.sql** - Main database schema including tables, indexes, RLS policies, and triggers
- **02_seed.sql** - Optional sample data for testing (commented out by default)

## Setup Instructions

### 1. Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign in or create an account
3. Click "New Project"
4. Enter project details and remember your database password
5. Wait for the project to be provisioned

### 2. Run Migration Scripts

1. In your Supabase project dashboard, click on the **SQL Editor** in the left sidebar
2. Click "New Query"
3. Copy the entire contents of `01_schema.sql`
4. Paste into the SQL editor
5. Click "Run" or press `Ctrl+Enter`
6. Verify all commands executed successfully (you should see green checkmarks)

### 3. Get Your Supabase Credentials

1. In the Supabase dashboard, click on **Settings** (gear icon) in the left sidebar
2. Click on **API** under Project Settings
3. You'll need:
   - **Project URL** (under "Config")
   - **anon public** key (under "Project API keys")
4. Copy these values for your `.streamlit/secrets.toml` file

### 4. Configure Authentication

By default, Supabase Auth is enabled. You can configure it further:

1. Go to **Authentication** > **Providers** in the Supabase dashboard
2. Email auth is enabled by default
3. Optional: Enable other providers (Google, GitHub, etc.)
4. Go to **Authentication** > **URL Configuration** to set redirect URLs if deploying

### 5. Optional: Add Sample Data

If you want to test with sample data:

1. Uncomment the relevant INSERT statements in `02_seed.sql`
2. Create a test user first via the Authentication UI or API
3. Update the UUIDs in the sample data to match your test user's ID
4. Run the modified `02_seed.sql` in the SQL Editor

## Database Schema Overview

### Tables

- **profiles** - User profiles (extends auth.users)
- **communities** - Community groups for shared forecasting
- **community_members** - Junction table for community membership
- **records** - Surf session records with all tracking data

### Row Level Security (RLS)

All tables have RLS enabled with policies to ensure:
- Users can only see/edit their own data
- Private records are only visible to the owner
- Public records are visible to everyone
- Community records are visible to community members
- Proper ownership checks for communities

### Automatic Features

- Auto-creation of user profiles when users sign up
- Automatic timestamp updates via triggers
- UUID primary keys for all tables
- Foreign key constraints for data integrity

## Troubleshooting

### "relation does not exist" error
- Make sure you ran `01_schema.sql` completely
- Check that all CREATE statements executed successfully

### RLS policy errors
- Ensure you're authenticated when testing queries
- Check that the `auth.uid()` function is available
- Verify RLS is enabled on tables: `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`

### Profile not auto-created
- Check that the `on_auth_user_created` trigger exists
- Verify the trigger function has `SECURITY DEFINER` set
- Look in the Supabase logs for any error messages

## Next Steps

After setting up the database:

1. Update `.streamlit/secrets.toml` with your Supabase credentials
2. Install the Supabase Python client: `pip install supabase`
3. Run the refactored Streamlit application
4. Test signup, login, and record creation
