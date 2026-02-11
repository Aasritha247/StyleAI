@echo off
echo Installing StyleAI+ Dependencies...
echo.

pip install flask opencv-python pillow numpy google-generativeai requests

echo.
echo Installation complete!
echo.
echo To run the application:
echo 1. Set your Gemini API key: set GEMINI_API_KEY=AIzaSyDD_xE-qG0pGZ9fDkqNGMClMSph3hz0p2Y
echo 2. Run: python server.py
echo 3. Open: http://localhost:5000
echo.
pause
