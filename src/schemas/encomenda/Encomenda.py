from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.encomenda.EncomendaStatus import EncomendaStatus
from schemas.encomenda.EncomendaLocalizacao import EncomendaLocalizacao
from schemas.encomenda.EncomendaHasProduto import EncomendaHasProduto
from schemas.produto.Produto import Produto

class Encomenda(BaseModel):
    encomenda_id: int = Field(examples=[1234], description="ID da encomenda", title="ID da encomenda")
    cliente_id: int = Field(examples=[123], description="ID do cliente", title="ID do cliente")
    descricao: Optional[str] = Field(default=None, examples=["Encomenda de produtos maneiros do Maciel"], description="Descrição da encomenda", title="Descrição da encomenda")
    valor_total: float = Field(examples=[100.0], description="Valor total da encomenda", title="Valor total da encomenda")
    status: Optional[str] = Field(default=EncomendaStatus.PENDENTE, examples=[EncomendaStatus.PENDENTE], description="Status da encomenda", title="Status da encomenda")
    
    localizacao_atual: Optional[EncomendaLocalizacao] = Field(examples=["Rua da Paz, 45"], description="Localização atual da encomenda", title="Localização atual da encomenda")

    produtos: Optional[List[EncomendaHasProduto]] = []

    class Config:
        orm_mode = True