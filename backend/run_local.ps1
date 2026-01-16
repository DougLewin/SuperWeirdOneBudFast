Write-Host "Starting API..." -ForegroundColor Green

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Edit .env with your Supabase credentials!" -ForegroundColor Yellow
    notepad .env
    exit
}

Write-Host "Server: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
uvicorn main:app --reload --host 0.0.0.0 --port 8000
