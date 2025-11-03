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

# Create a test file
test_file_path = "final_test_file.txt"
with open(test_file_path, "w") as f:
    f.write("This is a final test file for upload simulation")

# Simulate what happens in the API - directly save the file
nome_final = f"{int(time.time()*1000)}_final_test_file.txt"
caminho_fisico = os.path.join(MEDIA_DIR, nome_final)

print(f"Saving file to: {caminho_fisico}")

# Open the test file and save it directly
try:
    with open(test_file_path, "rb") as source_file:
        with open(caminho_fisico, "wb") as dest_file:
            shutil.copyfileobj(source_file, dest_file)
            
    # Check if file was saved
    file_size = os.path.getsize(caminho_fisico)
    print(f"✅ File saved successfully: {nome_final} ({file_size} bytes)")
    
    # List files in directory
    print("\nFiles in musicas directory:")
    for file in os.listdir(MEDIA_DIR):
        print(f"  {file}")
        
except Exception as e:
    print(f"❌ Error saving file: {e}")

# Clean up test files
os.remove(test_file_path)
if os.path.exists(caminho_fisico):
    os.remove(caminho_fisico)
    print(f"\nTest files cleaned up")