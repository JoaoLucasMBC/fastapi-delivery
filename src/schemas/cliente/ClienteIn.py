from pydantic import BaseModel, Field
from typing import Optional

class ClienteIn(BaseModel):
    nome: str = Field(examples=["João da Silva"], description="Nome do cliente", title="Nome do cliente")
    email: str = Field(examples=["joao@insper.edu.br"], description="Email do cliente", title="Email do cliente")
    cpf: str = Field(examples=["123.456.789-00"], description="CPF do cliente", title="CPF do cliente")
    telefone: str = Field(examples=["(11) 99999-9999"], description="Telefone do cliente", title="Telefone do cliente")
    endereco: str = Field(examples=["Rua da Paz, 45"], description="Endereço do cliente", title="Endereço do cliente")
    password: str = Field(examples=["123456"], description="Senha do cliente", title="Senha do cliente")