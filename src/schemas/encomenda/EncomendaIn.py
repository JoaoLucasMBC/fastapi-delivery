from pydantic import BaseModel, Field
from typing import Optional

class EncomendaIn(BaseModel):
    cliente_id: int = Field(examples=[123], description="ID do cliente", title="ID do cliente")
    descricao: Optional[str] = Field(default=None, examples=["Encomenda de produtos maneiros"], description="Descrição da encomenda", title="Descrição da encomenda")
    produtos: dict[str, int] = Field(examples=[{"produtoId": 123, "quantidade": 10}], description="Produtos da encomenda", title="Produtos da encomenda")
    localizacaoAtual: str = Field(examples=["Rua da Paz, 45"], description="Localização atual da encomenda", title="Localização atual da encomenda")