from pydantic import BaseModel, Field
from typing import Optional

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, examples=["Coca-Cola"], description="Nome do produto", title="Nome do produto")
    preco: Optional[float] = Field(default=None, examples=[5.0], description="Preço do produto", title="Preço do produto")
    descricao: Optional[str] = Field(default=None, examples=["Refrigerante de cola"], description="Descrição do produto", title="Descrição do produto")