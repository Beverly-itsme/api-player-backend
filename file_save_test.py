import os
import shutil
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

# Create a test file content
test_content = "This is a test file content for upload simulation"

# Test saving a file using the same approach as the API
nome_final = f"{int(time.time()*1000)}_test_file.txt"
caminho_fisico = os.path.join(MEDIA_DIR, nome_final)

print(f"Saving file to: {caminho_fisico}")

# Simulate saving file content (like what happens in the API)
try:
    # Create a file-like object with the content
    import io
    file_like_object = io.BytesIO(test_content.encode('utf-8'))
    
    # Save the file using shutil.copyfileobj (same as API)
    with open(caminho_fisico, "wb") as buffer:
        shutil.copyfileobj(file_like_object, buffer)
        
    # Check if file was saved
    file_size = os.path.getsize(caminho_fisico)
    print(f"✅ File saved successfully: {nome_final} ({file_size} bytes)")
    
    # List files in directory
    print("\nFiles in musicas directory:")
    for file in os.listdir(MEDIA_DIR):
        print(f"  {file}")
        
except Exception as e:
    print(f"❌ Error saving file: {e}")

# Clean up test file
if os.path.exists(caminho_fisico):
    os.remove(caminho_fisico)
    print(f"\nTest file cleaned up: {caminho_fisico}")