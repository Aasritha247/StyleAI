print("Testing imports...")

print("1. Testing Flask...")
try:
    import flask
    print("   ✓ Flask OK")
except Exception as e:
    print(f"   ✗ Flask ERROR: {e}")

print("2. Testing OpenCV...")
try:
    import cv2
    print("   ✓ OpenCV OK")
except Exception as e:
    print(f"   ✗ OpenCV ERROR: {e}")

print("3. Testing Pillow...")
try:
    from PIL import Image
    print("   ✓ Pillow OK")
except Exception as e:
    print(f"   ✗ Pillow ERROR: {e}")

print("4. Testing NumPy...")
try:
    import numpy
    print("   ✓ NumPy OK")
except Exception as e:
    print(f"   ✗ NumPy ERROR: {e}")

print("5. Testing Google AI...")
try:
    import google.generativeai
    print("   ✓ Google AI OK")
except Exception as e:
    print(f"   ✗ Google AI ERROR: {e}")

print("\nAll tests complete!")
