from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), index=True)
    email = Column(String(200), index=True)
    cpf = Column(String(14), index=True, unique=True)
    telefone = Column(String(200), index=True)
    endereco = Column(String(200), index=True)
    hash_password = Column(String(200), index=True)
    status = Column(String(36), index=True, default="ATIVO")
    data_cadastro = Column(DateTime, default=datetime.now())

    encomendas = relationship("Encomenda", back_populates="cliente")
    
    def __repr__(self):
        return f"<Cliente(clienteId={self.clienteId}, nome={self.nome}, email={self.email}, cpf={self.cpf}, telefone={self.telefone}, endereco={self.endereco}, hash_password={self.hash_password}, status={self.status})>"
    

class Produto(Base):
    __tablename__ = "produtos"

    produto_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), index=True)
    preco = Column(Float, index=True)
    descricao = Column(String(200), index=True, nullable=True)
    ultima_atualizacao = Column(DateTime, default=datetime.now())

    status = Column(String(36), index=True, default="ATIVO")
    
    def __repr__(self):
        return f"<Produto(produtoId={self.produtoId}, nome={self.nome}, preco={self.preco}, descricao={self.descricao}, ultima_atualizacao={self.ultima_atualizacao})>"
    

class Encomenda(Base):
    __tablename__ = "encomendas"

    encomenda_id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.cliente_id"))
    descricao = Column(String(200), index=True, nullable=True)
    valor_total = Column(Float, index=True)
    status = Column(String(36), index=True, default="PENDENTE")
    localizacao_atual_id = Column(Integer, ForeignKey("encomendas_localizacoes.localizacao_id"), nullable=True)

    localizacao_atual = relationship("EncomendaLocalizacao", foreign_keys=[localizacao_atual_id])
    cliente = relationship("Cliente", back_populates="encomendas", foreign_keys=[cliente_id])
    produtos = relationship("EncomendaProduto")

    def __repr__(self):
        return f"<Encomenda(encomendaId={self.encomendaId}, clienteId={self.clienteId}, descricao={self.descricao}, valorTotal={self.valorTotal}, localizacaoAtual={self.localizacaoAtual}, status={self.status})>"
    

class EncomendaProduto(Base):
    __tablename__ = "encomendas_produtos"

    encomenda_id = Column(Integer, ForeignKey("encomendas.encomenda_id"), primary_key=True)
    produto_id = Column(Integer, ForeignKey("produtos.produto_id"), primary_key=True)
    quantidade = Column(Integer, index=True)
    
    def __repr__(self):
        return f"<EncomendaProduto(encomendaId={self.encomendaId}, produtoId={self.produtoId})>"
    

class EncomendaLocalizacao(Base):
    __tablename__ = "encomendas_localizacoes"

    localizacao_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    encomenda_id = Column(Integer, ForeignKey("encomendas.encomenda_id"), primary_key=True)
    localizacao = Column(String(200), index=True)
    data = Column(DateTime, default=datetime.now())
    
    def __repr__(self):
        return f"<EncomendaLocalizacao(encomendaId={self.encomendaId}, localizacao={self.localizacao}, data={self.data})>"