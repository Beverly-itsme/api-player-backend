import os
import time

# Test the directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media", "musicas")
IMAGES_DIR = os.path.join(BASE_DIR, "media", "images")

print(f"Base directory: {BASE_DIR}")
print(f"Media directory: {MEDIA_DIR}")
print(f"Images directory: {IMAGES_DIR}")

# Ensure directories exist
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

print(f"Media directory exists: {os.path.exists(MEDIA_DIR)}")
print(f"Images directory exists: {os.path.exists(IMAGES_DIR)}")

# Create a test file in musicas directory directly
test_music_file = os.path.join(MEDIA_DIR, f"direct_test_{int(time.time())}_music.txt")
with open(test_music_file, "w") as f:
    f.write("This is a direct test music file")

print(f"Direct test music file created: {os.path.exists(test_music_file)}")

# Create a test file in images directory directly
test_image_file = os.path.join(IMAGES_DIR, f"direct_test_{int(time.time())}_image.jpg")
with open(test_image_file, "w") as f:
    f.write("This is a direct test image file")

print(f"Direct test image file created: {os.path.exists(test_image_file)}")

# List files in directories
print("\nFiles in musicas directory:")
for file in os.listdir(MEDIA_DIR):
    print(f"  {file}")

print("\nFiles in images directory:")
for file in os.listdir(IMAGES_DIR):
    print(f"  {file}")

# Clean up test files
os.remove(test_music_file)
os.remove(test_image_file)
print("\nDirect test files cleaned up.")