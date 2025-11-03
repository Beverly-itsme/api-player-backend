import requests
import json

try:
    response = requests.get('http://192.168.43.81:8000/musicas/')
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Content: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Number of music entries: {len(data)}")
        print("First few entries:")
        for i, entry in enumerate(data[:3]):
            print(f"  {i+1}. {entry['titulo']} - {entry.get('imagem', 'No image')}")
    else:
        print(f"Error: {response.status_code}")
        
except Exception as e:
    print(f"Exception occurred: {e}")