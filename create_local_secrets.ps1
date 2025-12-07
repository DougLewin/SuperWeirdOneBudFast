# Create Local Secrets File for Development
# This script helps you set up your local .streamlit/secrets.toml file

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Create Local Secrets File" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$secretsPath = ".streamlit\secrets.toml"

# Check if secrets.toml already exists
if (Test-Path $secretsPath) {
    Write-Host "⚠️  Warning: $secretsPath already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (yes/no)"
    if ($overwrite -ne "yes") {
        Write-Host "❌ Cancelled. No changes made." -ForegroundColor Red
        exit
    }
}

Write-Host ""
Write-Host "Please enter your credentials:" -ForegroundColor Green
Write-Host "(Press Enter to skip any optional fields)" -ForegroundColor Gray
Write-Host ""

# Get AWS credentials
Write-Host "AWS S3 Credentials (required for app to work):" -ForegroundColor Yellow
$awsKeyId = Read-Host "AWS_ACCESS_KEY_ID"
$awsSecretKey = Read-Host "AWS_SECRET_ACCESS_KEY" -AsSecureString
$awsSecretKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($awsSecretKey)
)

Write-Host ""
Write-Host "Google Gemini API Key (optional - for chatbot):" -ForegroundColor Yellow
$geminiKey = Read-Host "GEMINI_API_KEY (or leave blank to skip)"

# Create the secrets.toml content
$secretsContent = @"
# Local Streamlit Secrets
# WARNING: Never commit this file to version control!
# It is already in .gitignore

# AWS S3 Credentials
AWS_ACCESS_KEY_ID = "$awsKeyId"
AWS_SECRET_ACCESS_KEY = "$awsSecretKeyPlain"
"@

# Add Gemini key if provided
if ($geminiKey -and $geminiKey.Trim() -ne "") {
    $secretsContent += @"


# Google Gemini API Key (for chatbot)
GEMINI_API_KEY = "$geminiKey"
"@
}

# Write the file
try {
    $secretsContent | Out-File -FilePath $secretsPath -Encoding UTF8
    Write-Host ""
    Write-Host "✅ Success! Secrets file created at: $secretsPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Note: This file is in .gitignore and will NOT be committed to git" -ForegroundColor Cyan
    Write-Host ""
    
    if (-not $geminiKey -or $geminiKey.Trim() -eq "") {
        Write-Host "⚠️  Chatbot will be disabled (no GEMINI_API_KEY provided)" -ForegroundColor Yellow
        Write-Host "   You can add it later by editing .streamlit\secrets.toml" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "🚀 You can now run the app locally with: .\run_local.ps1" -ForegroundColor Green
    
} catch {
    Write-Host ""
    Write-Host "❌ Error creating secrets file: $_" -ForegroundColor Red
    exit 1
}
