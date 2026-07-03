# Resume Analyzer Run Script for Windows (PowerShell)
# This script starts the Flask backend and React frontend concurrently.

$ErrorActionPreference = "Stop"

# Clear host and print a welcome banner
Clear-Host
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   AI Resume Analyzer + Job Matcher Runner   " -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Store original working directory
$originalLocation = Get-Location

# Initialize backendProcess variable
$backendProcess = $null

try {
    # 1. Dependency checks
    Write-Host "[1/3] Checking prerequisites..." -ForegroundColor Gray

    # Check Node.js / npm
    if (-not (Get-Command "npm" -ErrorAction SilentlyContinue)) {
        Write-Host "Error: npm (Node Package Manager) is not installed or not in your PATH." -ForegroundColor Red
        Write-Host "Please install Node.js from https://nodejs.org/ and try again." -ForegroundColor Yellow
        exit 1
    }
    Write-Host "[OK] npm is installed." -ForegroundColor Green

    # Check Backend Python Virtual Environment
    $backendDir = Join-Path $PSScriptRoot "backend"
    $backendVenvPython = Join-Path $backendDir "venv\Scripts\python.exe"

    if (-not (Test-Path $backendVenvPython)) {
        Write-Host "Backend virtual environment not found at backend/venv. Attempting auto-setup..." -ForegroundColor Yellow
        
        # Verify Python is available
        if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
            Write-Host "Error: Python is not installed or not in your PATH." -ForegroundColor Red
            Write-Host "Please install Python 3.10+ and make sure it is added to your PATH." -ForegroundColor Yellow
            exit 1
        }
        
        Write-Host "Creating virtual environment in backend/venv..." -ForegroundColor Cyan
        Set-Location $backendDir
        Start-Process -FilePath "python" -ArgumentList "-m venv venv" -Wait
        
        if (-not (Test-Path $backendVenvPython)) {
            Write-Host "Error: Failed to create virtual environment." -ForegroundColor Red
            exit 1
        }
        
        Write-Host "Installing backend requirements..." -ForegroundColor Cyan
        $pipPath = Join-Path $backendDir "venv\Scripts\pip.exe"
        Start-Process -FilePath $pipPath -ArgumentList "install -r requirements.txt" -Wait
        
        Write-Host "Downloading spaCy NLP model..." -ForegroundColor Cyan
        $pythonVenvPath = Join-Path $backendDir "venv\Scripts\python.exe"
        Start-Process -FilePath $pythonVenvPath -ArgumentList "-m spacy download en_core_web_sm" -Wait
    }
    Write-Host "[OK] Backend Python virtual environment is ready." -ForegroundColor Green

    # Check Frontend node_modules
    $frontendDir = Join-Path $PSScriptRoot "frontend"
    $nodeModulesDir = Join-Path $frontendDir "node_modules"
    if (-not (Test-Path $nodeModulesDir)) {
        Write-Host "Frontend node_modules not found. Running 'npm install' first... This may take a few minutes." -ForegroundColor Yellow
        Set-Location $frontendDir
        Start-Process -FilePath "npm" -ArgumentList "install" -Wait
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error: npm install failed." -ForegroundColor Red
            exit 1
        }
        Write-Host "[OK] Frontend dependencies installed successfully." -ForegroundColor Green
    }
    Write-Host "[OK] Frontend dependencies are ready." -ForegroundColor Green
    Write-Host ""

    # 2. Starting Flask Backend
    Write-Host "[2/3] Starting Flask backend server..." -ForegroundColor Gray
    # Spawning the backend in a separate terminal window so its logs don't clutter the React dev server
    $backendProcess = Start-Process -FilePath $backendVenvPython -ArgumentList "app.py" -WorkingDirectory $backendDir -PassThru
    Start-Sleep -Seconds 2

    if ($backendProcess.HasExited) {
        Write-Host "Error: Flask backend failed to start. Please check the logs in the separate window." -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Flask backend started successfully (PID: $($backendProcess.Id)) on http://localhost:5000" -ForegroundColor Green
    Write-Host ""

    # 3. Starting React Frontend
    Write-Host "[3/3] Starting React frontend server..." -ForegroundColor Gray
    Write-Host "Starting npm run dev in this window..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C in this terminal to stop both servers." -ForegroundColor Yellow
    Write-Host "---------------------------------------------" -ForegroundColor Gray

    Set-Location $frontendDir
    npm run dev
}
catch {
    Write-Host "An error occurred: $_" -ForegroundColor Red
}
finally {
    # Cleanup: Kill the backend process when the frontend script finishes or is interrupted
    Write-Host ""
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host "Shutting down servers..." -ForegroundColor Yellow
    
    if ($null -ne $backendProcess -and -not $backendProcess.HasExited) {
        Write-Host "Stopping Flask backend (PID: $($backendProcess.Id))..." -ForegroundColor Yellow
        Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
    }
    
    Set-Location $originalLocation
    Write-Host "[OK] Cleaned up all services. Goodbye!" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Cyan
}
