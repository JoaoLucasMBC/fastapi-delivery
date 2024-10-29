from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class EncomendaHasProduto(BaseModel):
    encomenda_id: int = Field(examples=[1234], description="ID da encomenda", title="ID da encomenda")
    produto_id: int = Field(examples=[123], description="ID do produto", title="ID do produto")
    quantidade: int = Field(examples=[10], description="Quantidade do produto", title="Quantidade do produto")

    class Config:
        orm_mode = True