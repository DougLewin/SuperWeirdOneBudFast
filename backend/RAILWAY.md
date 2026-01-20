# Railway Deployment Guide

## Quick Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Railway deployment ready"
   git push
   ```

2. **Create Railway Project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect the Dockerfile

3. **Add Environment Variables**
   In Railway dashboard, go to Variables tab and add:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   ```

4. **Deploy**
   - Railway will automatically deploy
   - Your API will be at: `https://your-app.up.railway.app`

## Verify Deployment

- Health: `https://your-app.up.railway.app/health`
- Docs: `https://your-app.up.railway.app/docs`
- Root: `https://your-app.up.railway.app/`

## Troubleshooting

**App crashes?**
- Check Railway logs for errors
- Verify environment variables are set
- Ensure Supabase credentials are correct

**Port issues?**
- Railway automatically sets PORT - no config needed
- The app uses `${PORT:-8000}`

**Build fails?**
- Check that all 3 Python files are committed: `main.py`, `models.py`, `db.py`
- Verify `requirements.txt` is present
