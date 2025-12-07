# Streamlit Cloud Deployment Guide

## 🚀 Deploy to Streamlit Cloud

This guide walks you through deploying **Super Weird One Bud** to Streamlit Cloud.

---

## Prerequisites

- [ ] GitHub repository with your code
- [ ] AWS S3 bucket (`superweirdonebud`) with proper permissions
- [ ] AWS Access Key ID and Secret Access Key

---

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure these files are committed to your GitHub repository:
- `superweirdonebud.py` (main app)
- `requirements.txt` (dependencies)
- `.gitignore` (excludes secrets)

**DO NOT commit:**
- `.streamlit/secrets.toml` (local secrets file)
- AWS credentials
- Virtual environment folders

### 2. Create Streamlit Cloud Account

1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### 3. Deploy Your App

1. Click **"New app"** button
2. Select your repository: `DougLewin/SuperWeirdOneBud`
3. Choose branch: `main`
4. Set main file path: `superweirdonebud.py`
5. Click **"Deploy!"**

**Note**: The app will fail initially - this is expected! We need to add secrets first.

### 4. Configure AWS Secrets

This is **CRITICAL** - your app won't work without these!

1. In Streamlit Cloud, go to your app's settings (click the hamburger menu ☰)
2. Navigate to **"Secrets"** section
3. Add your AWS credentials in TOML format:

```toml
# Paste this into the Streamlit Cloud Secrets editor
# Replace the values with your actual AWS credentials

AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY_ID_HERE"
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_ACCESS_KEY_HERE"
```

4. Click **"Save"**
5. The app will automatically redeploy with the new secrets

### 5. Get Your AWS Credentials

If you don't have AWS credentials yet:

1. Log into AWS Console: https://console.aws.amazon.com/
2. Navigate to **IAM → Users → [Your User]**
3. Go to **"Security credentials"** tab
4. Click **"Create access key"**
5. Select use case: **"Application running outside AWS"**
6. Copy both:
   - Access Key ID
   - Secret Access Key (⚠️ save immediately - you can't view it again!)

### 6. Verify S3 Permissions

Your AWS user needs these S3 permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:ListBucket"
        ],
        "Resource": [
            "arn:aws:s3:::superweirdonebud",
            "arn:aws:s3:::superweirdonebud/*"
        ]
    }]
}
```

---

## Testing Your Deployment

1. Wait for the app to finish deploying (usually 1-2 minutes)
2. Access your app at: `https://[your-app-name].streamlit.app`
3. Test these features:
   - [ ] App loads without AWS errors
   - [ ] Can view existing records (data loads from S3)
   - [ ] Can create a new record
   - [ ] Can edit a record (password: `utfs`)
   - [ ] Can delete a record
   - [ ] Changes persist after page refresh (S3 is working)

---

## Troubleshooting

### ❌ "Failed to connect to AWS S3"

**Problem**: AWS credentials not configured correctly

**Solutions**:
1. Verify secrets are in Streamlit Cloud (Settings → Secrets)
2. Check for typos in `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
3. Ensure no extra spaces or quotes in the secret values
4. Make sure the secret names match exactly (case-sensitive)

### ❌ "InvalidAccessKeyId" or "SignatureDoesNotMatch"

**Problem**: Invalid AWS credentials

**Solutions**:
1. Create new AWS access keys
2. Update the secrets in Streamlit Cloud
3. Ensure you copied the entire key (no truncation)

### ❌ "NoSuchKey" or "NoSuchBucket"

**Problem**: S3 bucket or file doesn't exist

**Solutions**:
1. Verify bucket name is `superweirdonebud`
2. Check the bucket is in `ap-southeast-2` region
3. Create the bucket if it doesn't exist
4. The app will create `Rotto_Tracker.csv` automatically when you add the first record

### ⚠️ App won't start or keeps restarting

**Solutions**:
1. Check Streamlit Cloud logs (hamburger menu → Manage app → Logs)
2. Verify `requirements.txt` has correct package versions
3. Look for Python syntax errors in the logs
4. Try clicking "Reboot app" in settings

### 🔄 Changes not appearing

**Solutions**:
1. Push changes to GitHub
2. Streamlit Cloud auto-deploys from `main` branch
3. Force redeploy: Settings → Reboot app
4. Clear cache: hamburger menu → Clear cache

---

## App Settings on Streamlit Cloud

Recommended settings:

- **Python version**: 3.10 (auto-detected from requirements)
- **Always rerun**: On (recommended for multi-user access)
- **Secrets**: Configure as shown above

---

## Security Best Practices

✅ **DO:**
- Use IAM user with minimal S3 permissions (only this bucket)
- Rotate AWS access keys periodically
- Monitor AWS CloudWatch for unusual activity
- Use Streamlit Cloud secrets for credentials

❌ **DON'T:**
- Commit AWS credentials to GitHub
- Share your Streamlit Cloud secrets publicly
- Use root AWS account credentials
- Hardcode passwords (consider environment variables for edit password too)

---

## Monitoring & Maintenance

### Check S3 Usage
```bash
aws s3 ls s3://superweirdonebud/ --profile doug-personal
```

### Download S3 Backup
```bash
aws s3 cp s3://superweirdonebud/Rotto_Tracker.csv ./backup/ --profile doug-personal
```

### View App Analytics
- Streamlit Cloud provides basic analytics
- See viewer count and app status in dashboard

---

## Cost Considerations

**Streamlit Cloud:**
- Free tier: 1 private app (unlimited public apps)
- Auto-sleeps after inactivity
- Wakes on first visit

**AWS S3:**
- Free tier: 5GB storage, 20,000 GET requests, 2,000 PUT requests/month
- This app uses minimal storage (~few KB for CSV file)
- Expect $0.00 - $0.01/month for typical usage

---

## Updating Your App

1. Make changes locally and test with `.\run_local.ps1`
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
3. Streamlit Cloud auto-deploys within 1-2 minutes
4. Check deployment status in Streamlit Cloud dashboard

---

## Advanced: Multiple Environments

You can deploy different branches for testing:

- **Production**: Deploy from `main` branch
- **Staging**: Deploy from `staging` branch with separate S3 bucket
- **Development**: Run locally with `.\run_local.ps1`

Each deployment can have different secrets configured.

---

## Support Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **Streamlit Community**: https://discuss.streamlit.io/
- **AWS S3 Documentation**: https://docs.aws.amazon.com/s3/
- **This Project's Setup Guide**: See `SETUP.md` for local development

---

## Quick Reference

### Streamlit Cloud URL Structure
```
https://[username]-[repo-name]-[app-name]-[random].streamlit.app
```

### Required Secrets Format
```toml
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

### App Password
Edit password (in-app): `utfs` or `utsf`

---

## ✅ Deployment Checklist

Before going live:

- [ ] Code pushed to GitHub `main` branch
- [ ] `requirements.txt` contains all dependencies
- [ ] `.gitignore` excludes secrets and venv
- [ ] AWS S3 bucket exists and is accessible
- [ ] AWS credentials configured in Streamlit Cloud Secrets
- [ ] App deployed and running on Streamlit Cloud
- [ ] All features tested (create, edit, delete, filter)
- [ ] Data persists in S3 after changes
- [ ] No errors in Streamlit Cloud logs

---

**🎉 You're ready to surf! 🏄‍♂️**

Last Updated: December 7, 2025
