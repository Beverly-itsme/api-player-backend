import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'media.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Delete music entries with IDs 12 to 16
    for id in range(12, 17):
        cursor.execute('DELETE FROM musicas WHERE id = ?', (id,))
        print(f"Deleted music entry with ID {id}")
    
    # Commit changes
    conn.commit()
    print(f"\nSuccessfully deleted music entries with IDs 12-16")
    
    # Verify deletion by listing remaining entries
    cursor.execute('SELECT id, titulo FROM musicas')
    rows = cursor.fetchall()
    print(f"\nRemaining music entries:")
    print(f"ID | Title")
    print(f"----------------------------------------")
    for row in rows:
        print(f"{row[0]} | {row[1]}")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()