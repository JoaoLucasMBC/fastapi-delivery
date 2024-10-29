from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.produto.ProdutoIn import ProdutoIn
from schemas.produto.ProdutoUpdate import ProdutoUpdate
from datetime import datetime

class Produto(BaseModel):
    produto_id: int = Field(examples=[12], description="Identificador único do produto", title="Identificador único do produto")
    nome: str = Field(examples=["Coca-Cola"], description="Nome do produto", title="Nome do produto")
    preco: float = Field(examples=[5.0], description="Preço do produto", title="Preço do produto")
    descricao: Optional[str] = Field(default=None, examples=["Refrigerante de cola"], description="Descrição do produto", title="Descrição do produto")
    ultima_atualizacao: Optional[datetime] = Field(default=None, examples=[datetime.now()], description="Data da última atualização do produto", title="Data da última atualização do produto")
    status: Optional[str] = Field(default="ATIVO", examples=["ATIVO"], description="Status do produto", title="Status do produto")

    class Config:
        orm_mode = True