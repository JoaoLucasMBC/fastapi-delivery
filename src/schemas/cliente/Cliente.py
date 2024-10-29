from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from schemas.cliente.ClienteStatus import ClienteStatus
from schemas.encomenda.Encomenda import Encomenda
import bcrypt

class Cliente(BaseModel):
    cliente_id: int = Field(examples=[123], description="Id do cliente", title="Id do cliente")
    nome: str = Field(examples=["João da Silva"], description="Nome do cliente", title="Nome do cliente")
    email: str = Field(examples=["joao@insper.edu.br"], description="Email do cliente", title="Email do cliente")
    cpf: str = Field(examples=["123.456.789-00"], description="CPF do cliente", title="CPF do cliente")
    telefone: str = Field(examples=["(11) 99999-9999"], description="Telefone do cliente", title="Telefone do cliente")
    endereco: str = Field(examples=["Rua da Paz, 45"], description="Endereço do cliente", title="Endereço do cliente")
    hash_password: str = Field(
        examples=["$2b$12$z7P1Q3z6u8QsZo5Q0zJH7e5WzF7d2Q1Q2z4Q3z6u8QsZo5Q0zJH7e5WzF7d2Q1Q2z4Q3z6u8QsZo5Q0zJH7e5WzF7d2Q1Q2"], 
        description="Senha do cliente encriptada para manter a segurança da aplicação", 
        title="Senha do cliente"
    )
    data_cadastro: Optional[datetime] = Field(default=datetime.now(), examples=["2021-09-01T00:00:00"], description="Data de cadastro do cliente", title="Data de cadastro do cliente")
    status: Optional[ClienteStatus] = Field(
        default=ClienteStatus.ATIVO, 
        examples=["ATIVO"], 
        description="Status do cliente. A deleção dos clientes é lógica. Ele nunca é deletado, apenas marcado como inativo.", 
        title="Status do cliente"
    )

    class Config:
        orm_mode = True

    @staticmethod
    def hash_pswd(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(Cliente.hash_pswd(password), self.hash_password)