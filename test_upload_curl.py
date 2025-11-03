import requests
import os

# Create a small test file
test_file_path = "test_upload.txt"
with open(test_file_path, "w") as f:
    f.write("This is a test file for upload")

# Test file upload
url = "http://192.168.43.81:8000/musicas/"

# Prepare the files for upload
files = {
    "arquivo": (test_file_path, open(test_file_path, "rb"), "text/plain"),
    "imagem": (test_file_path, open(test_file_path, "rb"), "text/plain")
}

data = {
    "titulo": "Curl Test Song",
    "artista": "Curl Test Artist",
    "letra": "Curl test lyrics"
}

try:
    response = requests.post(url, files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Check if files were created
    print("\nChecking if files were created:")
    import time
    time.sleep(2)  # Wait a bit for file creation
    
    # Check musicas directory
    musicas_files = os.listdir("media/musicas")
    print(f"Musicas files: {len(musicas_files)}")
    
    # Check images directory
    images_files = os.listdir("media/images")
    print(f"Images files: {len(images_files)}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close file handles
    for file_tuple in files.values():
        file_tuple[1].close()
    
    # Clean up test file
    if os.path.exists(test_file_path):
        os.remove(test_file_path)