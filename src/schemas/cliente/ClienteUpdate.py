from pydantic import BaseModel, Field
from typing import Optional

class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, examples=["João da Silva"], description="Nome do cliente", title="Nome do cliente")
    email: Optional[str] = Field(default=None, examples=["joao@insper.edu.br"], description="Email do cliente", title="Email do cliente")
    cpf: Optional[str] = Field(default=None, examples=["123.456.789-00"], description="CPF do cliente", title="CPF do cliente")
    telefone: Optional[str] = Field(default=None, examples=["(11) 99999-9999"], description="Telefone do cliente", title="Telefone do cliente")
    endereco: Optional[str] = Field(default=None, examples=["Rua da Paz, 45"], description="Endereço do cliente", title="Endereço do cliente")
    password: Optional[str] = Field(default=None, examples=["123456"], description="Senha do cliente", title="Senha do cliente")