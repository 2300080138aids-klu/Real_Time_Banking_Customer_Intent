Write-Host "====================================="
Write-Host "  Banking Intent Detection System"
Write-Host "====================================="

# Environment variables
$env:HF_HUB_DISABLE_SYMLINKS_WARNING="1"
$env:TRANSFORMERS_NO_ADVISORY_WARNINGS="1"

# Production startup
uvicorn app.main:app `
    --host 0.0.0.0 `
    --port 8000 `
    --workers 2 `
    --log-level warning