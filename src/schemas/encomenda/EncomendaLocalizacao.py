from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from schemas.encomenda.EncomendaIn import EncomendaIn

class EncomendaLocalizacao(BaseModel):
    encomenda_id: int = Field(examples=[1234], description="ID da encomenda", title="ID da encomenda")
    localizacao: str = Field(examples=["Rua da Paz, 45"], description="Localização da encomenda", title="Localização da encomenda")
    data: datetime = Field(default=datetime.now(), examples=[datetime.now()], description="Data do registro da localização", title="Data do registro da localização")

    class Config:
        orm_mode = True