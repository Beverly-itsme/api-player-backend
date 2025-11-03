from pydantic import BaseModel
from typing import Optional

class MusicaBase(BaseModel):
    titulo: str
    artista: str
    letra: Optional[str] = None

class MusicaCreate(MusicaBase):
    pass

class Musica(MusicaBase):
    id: int
    arquivo: str
    imagem: Optional[str] = None

    class Config:
        from_attributes = True

class VideoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    id: int
    arquivo: str

    class Config:
        from_attributes = True