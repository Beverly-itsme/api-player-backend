from app.database import engine
from app import models

# This will add the new column to the existing table
models.Base.metadata.create_all(bind=engine)
print("Database updated successfully!")