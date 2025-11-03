import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Video, Base

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./media.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Get database session
db = SessionLocal()

# Get list of video files
video_dir = "media/videos"
try:
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    print(f"Found {len(video_files)} video files")
except FileNotFoundError:
    print(f"Directory {video_dir} not found")
    sys.exit(1)

# Update each video in database with full URL
updated_count = 0
for video_file in video_files:
    # Find video in database by filename
    video = db.query(Video).filter(Video.arquivo == video_file).first()
    if video:
        # Update with full URL
        full_url = f"http://192.168.43.81:8000/media/videos/{video_file}"
        video.arquivo = full_url
        updated_count += 1
        print(f"Updated {video_file} with URL: {full_url}")

# Commit changes
db.commit()
print(f"Updated {updated_count} videos with full URLs")

# Close database connection
db.close()