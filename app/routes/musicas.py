from fastapi import APIRouter, Depends, UploadFile, File, Form, Request, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app import models, schemas
from app.database import SessionLocal, engine
import shutil
import os
import unicodedata
import re
import time

models.Base.metadata.create_all(bind=engine)
router = APIRouter()

# =========================
# 🔹 Conexão com o banco
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
#  Diretórios
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, "media", "musicas")
IMAGES_DIR = os.path.join(BASE_DIR, "media", "images")

# Ensure directories exist
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

def normalizar_nome(nome):
    nome = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode('ascii')
    nome = re.sub(r'[^a-zA-Z0-9._-]', '_', nome)
    return nome


# =========================
#  CRUD de músicas
# =========================
@router.get("/", response_model=list[schemas.Musica])
def listar_musicas(request: Request, db: Session = Depends(get_db)):
    base_url = str(request.base_url).rstrip('/')
    musicas = db.query(models.Musica).all()
    result = []
    for m in musicas:
        # Create a dictionary with the music data
        musica_dict = {
            "id": m.id,
            "titulo": m.titulo,
            "artista": m.artista,
            "letra": m.letra,
            "arquivo": m.arquivo,
            "imagem": getattr(m, 'imagem', None)  # Safely get imagem attribute
        }
        
        # Handle audio file URL
        if musica_dict["arquivo"] and not str(musica_dict["arquivo"]).startswith('http'):
            musica_dict["arquivo"] = f"{base_url}/media/musicas/{os.path.basename(str(musica_dict['arquivo']))}"
        
        # Handle image URL
        if musica_dict["imagem"] and not str(musica_dict["imagem"]).startswith('http'):
            musica_dict["imagem"] = f"{base_url}/media/images/{os.path.basename(str(musica_dict['imagem']))}"
            
        result.append(musica_dict)
    return result


@router.post("/", response_model=schemas.Musica)
def adicionar_musica(
    request: Request,
    titulo: str = Form(...),
    artista: str = Form(...),
    letra: str = Form(""),
    imagem: UploadFile = File(None),  # Optional image upload
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Debug information
    print(f"Recebendo upload: {arquivo.filename}")
    print(f"Tipo de conteúdo: {getattr(arquivo, 'content_type', 'Desconhecido')}")
    
    # Save audio file
    nome_limpo = normalizar_nome(arquivo.filename)
    nome_final = f"{int(time.time()*1000)}_{nome_limpo}"
    caminho_fisico = os.path.join(MEDIA_DIR, nome_final)
    caminho_fisico_img = None

    print(f"Salvando áudio em: {caminho_fisico}")
    
    # Save the audio file directly without reading content first
    try:
        # Save the file directly using shutil.copyfileobj
        with open(caminho_fisico, "wb") as buffer:
            shutil.copyfileobj(arquivo.file, buffer)
            
        # Check if file was saved
        file_size = os.path.getsize(caminho_fisico)
        print(f"✅ Áudio salvo com sucesso: {nome_final} ({file_size} bytes)")
    except Exception as e:
        print(f"❌ Erro ao salvar áudio: {e}")
        raise

    base_url = str(request.base_url).rstrip('/')
    url_arquivo = f"{base_url}/media/musicas/{nome_final}"

    # Save image file if provided
    url_imagem = None
    nome_final_img = None
    if imagem and imagem.filename:
        # Debug information
        print(f"Recebendo imagem: {imagem.filename}")
        print(f"Tipo de conteúdo da imagem: {getattr(imagem, 'content_type', 'Desconhecido')}")
        
        # Ensure images directory exists
        os.makedirs(IMAGES_DIR, exist_ok=True)
        
        nome_limpo_img = normalizar_nome(imagem.filename)
        nome_final_img = f"{int(time.time()*1000)}_img_{nome_limpo_img}"
        caminho_fisico_img = os.path.join(IMAGES_DIR, nome_final_img)
        
        print(f"Salvando imagem em: {caminho_fisico_img}")

        # Save the image file directly without reading content first
        try:
            with open(caminho_fisico_img, "wb") as buffer:
                shutil.copyfileobj(imagem.file, buffer)
                
            # Check if file was saved
            image_size = os.path.getsize(caminho_fisico_img)
            print(f"✅ Imagem salva com sucesso: {nome_final_img} ({image_size} bytes)")
        except Exception as e:
            print(f"❌ Erro ao salvar imagem: {e}")
            raise

        url_imagem = f"{base_url}/media/images/{nome_final_img}"

    # Create the music record
    db_musica_data = {
        "titulo": titulo,
        "artista": artista,
        "letra": letra,
        "arquivo": url_arquivo
    }
    
    # Only add imagem if the column exists and we have an image
    if url_imagem:
        try:
            # Test if the column exists by trying to access it
            db.query(models.Musica).first()
            db_musica_data["imagem"] = url_imagem
        except OperationalError:
            # Column doesn't exist, skip it for now
            pass

    db_musica = models.Musica(**db_musica_data)
    db.add(db_musica)
    db.commit()
    db.refresh(db_musica)

    # Verify that files were saved correctly
    audio_saved = os.path.exists(caminho_fisico)
    image_saved = os.path.exists(caminho_fisico_img) if caminho_fisico_img else True
    
    if audio_saved and image_saved:
        print(f"✅ Música salva com sucesso: {titulo}")
        print(f"   Áudio: {nome_final} - Existe: {audio_saved}")
        print(f"   Imagem: {nome_final_img or 'Nenhuma'} - Existe: {image_saved}")
    else:
        print(f"❌ Erro ao salvar música: {titulo}")
        if not audio_saved:
            print(f"   Áudio não salvo: {nome_final}")
        if not image_saved:
            print(f"   Imagem não salva: {nome_final_img}")

    return db_musica


# =========================
#  Favoritos (corrigido e funcional)
# =========================

favoritos = []  # Usar lista é mais seguro e compatível com JSON

@router.get("/favoritas", response_model=list[schemas.Musica])
def listar_favoritas(request: Request, db: Session = Depends(get_db)):
    base_url = str(request.base_url).rstrip('/')
    if not favoritos:
        print(" Nenhum favorito salvo.")
        return []

    musicas = db.query(models.Musica).filter(models.Musica.id.in_(favoritos)).all()
    result = []
    for m in musicas:
        # Create a dictionary with the music data
        musica_dict = {
            "id": m.id,
            "titulo": m.titulo,
            "artista": m.artista,
            "letra": m.letra,
            "arquivo": m.arquivo,
            "imagem": getattr(m, 'imagem', None)  # Safely get imagem attribute
        }
        
        # Handle audio file URL
        if musica_dict["arquivo"] and not str(musica_dict["arquivo"]).startswith('http'):
            musica_dict["arquivo"] = f"{base_url}/media/musicas/{os.path.basename(str(musica_dict['arquivo']))}"
        
        # Handle image URL
        if musica_dict["imagem"] and not str(musica_dict["imagem"]).startswith('http'):
            musica_dict["imagem"] = f"{base_url}/media/images/{os.path.basename(str(musica_dict['imagem']))}"
            
        result.append(musica_dict)

    print(f"🎧 {len(result)} músicas favoritas listadas.")
    return result


#  Adicionar favorito por ID na URL
@router.post("/favoritas/{musica_id}")
def adicionar_favorita_url(musica_id: int, db: Session = Depends(get_db)):
    musica = db.query(models.Musica).filter(models.Musica.id == musica_id).first()
    if not musica:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    if musica_id in favoritos:
        raise HTTPException(status_code=400, detail="Já está nos favoritos")

    favoritos.append(musica_id)
    print(f" Adicionada aos favoritos: {musica.titulo}")
    return {"mensagem": "Música adicionada aos favoritos"}


#  Adicionar favorito via JSON body (para o React Native)
@router.post("/favoritas")
def adicionar_favorita_body(payload: dict = Body(...), db: Session = Depends(get_db)):
    musica_id = payload.get("id")
    if not musica_id:
        raise HTTPException(status_code=400, detail="Envie um JSON com {'id': <musica_id>}")
    
    musica = db.query(models.Musica).filter(models.Musica.id == musica_id).first()
    if not musica:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    if musica_id in favoritos:
        raise HTTPException(status_code=400, detail="Já está nos favoritos")

    favoritos.append(musica_id)
    print(f" Adicionada aos favoritos via JSON: {musica.titulo}")
    return {"mensagem": "Música adicionada aos favoritos"}


#  Remover favorito
@router.delete("/favoritas/{musica_id}")
def remover_favorita(musica_id: int):
    if musica_id not in favoritos:
        raise HTTPException(status_code=404, detail="Música não está nos favoritos")

    favoritos.remove(musica_id)
    print(f" Removida dos favoritos: ID {musica_id}")
    return {"mensagem": "Música removida dos favoritos"}
