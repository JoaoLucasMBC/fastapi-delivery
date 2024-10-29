from pydantic import BaseModel, Field
from typing import Optional

class ProdutoIn(BaseModel):
    nome: str = Field(examples=["Coca-Cola"], description="Nome do produto", title="Nome do produto")
    preco: float = Field(examples=[5.0], description="Preço do produto", title="Preço do produto")
    descricao: Optional[str] = Field(default=None, examples=["Refrigerante de cola"], description="Descrição do produto", title="Descrição do produto")