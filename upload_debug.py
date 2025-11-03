import os
import shutil
import time

# Test the directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media", "musicas")
IMAGES_DIR = os.path.join(BASE_DIR, "media", "images")

# Ensure directories exist
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Create a test file
test_file_path = "test_upload_file.txt"
with open(test_file_path, "w") as f:
    f.write("This is a test file for upload debugging")

# Simulate what happens in the API
print("Simulating file upload...")

# Read the file content
with open(test_file_path, "rb") as f:
    file_content = f.read()
    print(f"File content size: {len(file_content)} bytes")

# Create a file-like object (simulating UploadFile)
import io
file_like_object = io.BytesIO(file_content)

# Try to read the content
content1 = file_like_object.read()
print(f"First read: {len(content1)} bytes")

# Try to read again (this should return empty)
file_like_object.seek(0)  # Reset pointer
content2 = file_like_object.read()
print(f"Second read after seek(0): {len(content2)} bytes")

# Clean up
os.remove(test_file_path)