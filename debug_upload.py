import requests
import os

# Test file upload
url = "http://192.168.43.81:8000/musicas/"

# Create a small test audio file
test_audio_path = "test_audio.mp3"
with open(test_audio_path, "w") as f:
    f.write("This is a test audio file content")

# Create a small test image file
test_image_path = "test_image.jpg"
with open(test_image_path, "w") as f:
    f.write("This is a test image file content")

# Prepare the files for upload
files = {
    "arquivo": (test_audio_path, open(test_audio_path, "rb"), "audio/mpeg"),
    "imagem": (test_image_path, open(test_image_path, "rb"), "image/jpeg")
}

data = {
    "titulo": "Test Song",
    "artista": "Test Artist",
    "letra": "Test lyrics"
}

try:
    response = requests.post(url, files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close file handles
    for file_tuple in files.values():
        file_tuple[1].close()
    
    # Clean up test files
    if os.path.exists(test_audio_path):
        os.remove(test_audio_path)
    if os.path.exists(test_image_path):
        os.remove(test_image_path)