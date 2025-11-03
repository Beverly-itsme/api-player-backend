import os
import sys
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import the existing models
from app import models
from app.database import SQLALCHEMY_DATABASE_URL

def migrate_database():
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    
    # Check if the imagem column exists
    try:
        # Try to query the column
        result = engine.execute("PRAGMA table_info(musicas)")
        columns = [row[1] for row in result.fetchall()]
        
        if 'imagem' not in columns:
            print("Adding 'imagem' column to 'musicas' table...")
            # Add the column
            engine.execute("ALTER TABLE musicas ADD COLUMN imagem VARCHAR")
            print("Column added successfully!")
        else:
            print("Column 'imagem' already exists.")
            
    except Exception as e:
        print(f"Error during migration: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if migrate_database():
        print("Database migration completed successfully!")
    else:
        print("Database migration failed!")