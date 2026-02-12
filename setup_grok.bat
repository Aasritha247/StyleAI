@echo off
echo ========================================
echo StyleAI+ Setup with Grok API
echo ========================================
echo.

REM Check if .env exists
if exist .env (
    echo .env file already exists!
    echo.
) else (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo Please edit .env file and add your Grok API key!
    echo Get your key from: https://console.x.ai/
    echo.
)

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your XAI_API_KEY
echo 2. Run: python server_simple.py
echo 3. Open browser at: http://localhost:5000
echo.
echo For help, see ENV_SETUP.md
echo ========================================
pause
