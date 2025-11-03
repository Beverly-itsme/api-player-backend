import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'media.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Query the musicas table
    cursor.execute('SELECT id, titulo, arquivo, imagem FROM musicas')
    rows = cursor.fetchall()
    
    print('ID | Title | Audio Path | Image Path')
    print('-' * 80)
    for row in rows:
        print(f'{row[0]} | {row[1]} | {row[2]} | {row[3]}')
        
    print('\nChecking if media directories exist:')
    media_dir = os.path.join(os.path.dirname(__file__), 'media')
    musicas_dir = os.path.join(media_dir, 'musicas')
    images_dir = os.path.join(media_dir, 'images')
    
    print(f'Media directory exists: {os.path.exists(media_dir)}')
    print(f'Musicas directory exists: {os.path.exists(musicas_dir)}')
    print(f'Images directory exists: {os.path.exists(images_dir)}')
    
    if os.path.exists(musicas_dir):
        print(f'\nFiles in musicas directory:')
        for file in os.listdir(musicas_dir):
            print(f'  {file}')
            
    if os.path.exists(images_dir):
        print(f'\nFiles in images directory:')
        for file in os.listdir(images_dir):
            print(f'  {file}')
        
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()