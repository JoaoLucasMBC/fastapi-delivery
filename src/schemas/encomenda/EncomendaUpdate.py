from pydantic import BaseModel, Field
from typing import Optional

class EncomendaUpdate(BaseModel):
    clienteId: Optional[int] = Field(default=None, examples=[123], description="ID do cliente", title="ID do cliente")
    descricao: Optional[str] = Field(default=None, examples=["Encomenda de produtos maneiros"], description="Descrição da encomenda", title="Descrição da encomenda")
    produtos: Optional[dict[str, int]] = Field(default=None, examples=[{"produtoId": 123, "quantidade": 10}], description="Produtos da encomenda", title="Produtos da encomenda")
    localizacaoAtual: Optional[str] = Field(default=None, examples=["Rua da Paz, 45"], description="Localização atual da encomenda", title="Localização atual da encomenda")