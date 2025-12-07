# Local Development Secrets Configuration

## Quick Setup

To enable the chatbot (and AWS S3) for local development, create a secrets file:

### Option 1: Use the Setup Script (Recommended)

Run this PowerShell script to interactively create your secrets file:

```powershell
.\create_local_secrets.ps1
```

It will prompt you for:
- AWS Access Key ID (required)
- AWS Secret Access Key (required)
- Gemini API Key (optional - for chatbot)

### Option 2: Manual Creation

1. Create a new file at: `.streamlit\secrets.toml`

2. Add the following content (replace with your actual keys):

```toml
# Local Streamlit Secrets
# WARNING: Never commit this file to version control!

# AWS S3 Credentials
AWS_ACCESS_KEY_ID = "your-aws-access-key-here"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-key-here"

# Google Gemini API Key (for chatbot)
GEMINI_API_KEY = "your-gemini-api-key-here"
```

3. Save the file

## Where to Get API Keys

### AWS Credentials
- You should already have these from your initial setup
- Check your AWS IAM console or local AWS config

### Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it into `secrets.toml`

## Security Notes

✅ **Safe:**
- `.streamlit/secrets.toml` is in `.gitignore`
- This file will NOT be committed to GitHub
- It's only used for local development

❌ **Never:**
- Commit secrets to version control
- Share your secrets file
- Push secrets.toml to GitHub

## Verification

After creating the secrets file:

1. Run the app locally:
   ```powershell
   .\run_local.ps1
   ```

2. Check for these indicators:
   - ✅ No "AWS credentials" error → S3 is working
   - ✅ No "Gemini API key not found" warning → Chatbot is enabled
   - ✅ 💬 button appears in bottom-right → Chatbot UI is loaded

## Troubleshooting

### Chatbot Still Shows "Not Available"
- Check that `GEMINI_API_KEY` is spelled exactly right (case-sensitive)
- Ensure the key is enclosed in quotes: `"your-key"`
- Verify no extra spaces before/after the key
- Restart the Streamlit app

### AWS Errors
- Check AWS credentials are correct
- Ensure quotes around the values
- Verify AWS account has S3 permissions

### File Not Found
- Make sure the file is at: `.streamlit\secrets.toml` (with backslash on Windows)
- Check file extension is `.toml` not `.toml.txt`

## What's the Difference?

| Environment | Secrets Location |
|-------------|------------------|
| **Local Development** | `.streamlit/secrets.toml` (this file) |
| **Streamlit Cloud** | App Settings → Secrets (web interface) |

Both use the same TOML format, but are stored differently for security.
