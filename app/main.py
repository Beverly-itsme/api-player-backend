import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import musicas, videos

#  Inicializar a aplicação
app = FastAPI(title="Media Player API")

# Configurar CORS (for conactio to  Expo Go)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/app
ROOT_DIR = os.path.dirname(BASE_DIR)                   # backend/
MEDIA_DIR = os.path.join(ROOT_DIR, "media")            # backend/media

# Criar pastas se não existirem
os.makedirs(os.path.join(MEDIA_DIR, "musicas"), exist_ok=True)
os.makedirs(os.path.join(MEDIA_DIR, "videos"), exist_ok=True)

# Log para verificar no terminal
print(f"Servindo media de: {MEDIA_DIR}")

#  Servir arquivos estaticos (musicas e videos)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

#  Rotas
app.include_router(musicas.router, prefix="/musicas", tags=["Músicas"])
app.include_router(videos.router, prefix="/videos", tags=["Vídeos"])

#  Rota inicial
@app.get("/")
def root():
    return {"mensagem": " API do Media Player esta ativa!"}
