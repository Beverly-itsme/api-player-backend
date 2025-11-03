from fastapi import APIRouter, Depends, UploadFile, File, Form, Request, HTTPException, Body
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
import shutil
import os
import unicodedata
import re
import time

models.Base.metadata.create_all(bind=engine)
router = APIRouter()

#  Conexao com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Diretorio de midia
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, "media", "videos")
os.makedirs(MEDIA_DIR, exist_ok=True)

#  Funcao para limpar nome do arquivo
def normalizar_nome(nome):
    nome = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode('ascii')
    nome = re.sub(r'[^a-zA-Z0-9._-]', '_', nome)
    return nome

#  Listar videos
@router.get("/", response_model=list[schemas.Video])
def listar_videos(request: Request, db: Session = Depends(get_db)):
    """
    Retorna todos os vídeos com o link completo (URL absoluta).
    """
    base_url = str(request.base_url).rstrip('/')
    videos = db.query(models.Video).all()
    for v in videos:
        if v.arquivo and not str(v.arquivo).startswith('http'):
            v.arquivo = f"{base_url}/media/videos/{os.path.basename(v.arquivo)}"
    return videos

#  Adicionar novo video
@router.post("/", response_model=schemas.Video)
def adicionar_video(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(""),
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Faz upload de um novo video e salva no banco.
    """
    nome_limpo = normalizar_nome(arquivo.filename)
    nome_final = f"{int(time.time() * 1000)}_{nome_limpo}"
    caminho_fisico = os.path.join(MEDIA_DIR, nome_final)

    # Salvar o video no diretorio
    with open(caminho_fisico, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    # Criar URL publica
    base_url = str(request.base_url).rstrip('/')
    url_arquivo = f"{base_url}/media/videos/{nome_final}"

    # Salvar no banco de dados
    db_video = models.Video(
        titulo=titulo,
        descricao=descricao,
        arquivo=url_arquivo
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)

    print(f" Vídeo salvo: {titulo} -> {nome_final}")
    return db_video

# =========================
#  Favoritos (para vídeos)
# =========================

favoritos = []  # Usar lista é mais seguro e compatível com JSON

@router.get("/favoritas", response_model=list[schemas.Video])
def listar_favoritas(request: Request, db: Session = Depends(get_db)):
    base_url = str(request.base_url).rstrip('/')
    if not favoritos:
        print(" Nenhum vídeo favorito salvo.")
        return []

    videos = db.query(models.Video).filter(models.Video.id.in_(favoritos)).all()
    for v in videos:
        if v.arquivo and not str(v.arquivo).startswith('http'):
            v.arquivo = f"{base_url}/media/videos/{os.path.basename(v.arquivo)}"

    print(f" Vídeos favoritos listados: {len(videos)}")
    return videos

#  Adicionar favorito por ID na URL
@router.post("/favoritas/{video_id}")
def adicionar_favorita_url(video_id: int, db: Session = Depends(get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    if video_id in favoritos:
        raise HTTPException(status_code=400, detail="Já está nos favoritos")

    favoritos.append(video_id)
    print(f" Vídeo adicionado aos favoritos: {video.titulo}")
    return {"mensagem": "Vídeo adicionado aos favoritos"}

#  Adicionar favorito via JSON body (para o React Native)
@router.post("/favoritas")
def adicionar_favorita_body(payload: dict = Body(...), db: Session = Depends(get_db)):
    video_id = payload.get("id")
    if not video_id:
        raise HTTPException(status_code=400, detail="Envie um JSON com {'id': <video_id>}")
    
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    if video_id in favoritos:
        raise HTTPException(status_code=400, detail="Já está nos favoritos")

    favoritos.append(video_id)
    print(f" Vídeo adicionado aos favoritos via JSON: {video.titulo}")
    return {"mensagem": "Vídeo adicionado aos favoritos"}

#  Remover favorito
@router.delete("/favoritas/{video_id}")
def remover_favorita(video_id: int):
    if video_id not in favoritos:
        raise HTTPException(status_code=404, detail="Vídeo não está nos favoritos")

    favoritos.remove(video_id)
    print(f" Vídeo removido dos favoritos: ID {video_id}")
    return {"mensagem": "Vídeo removido dos favoritos"}