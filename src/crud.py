from datetime import datetime
from sqlalchemy.orm import Session

import models
from schemas.produto.ProdutoIn import ProdutoIn
from schemas.produto.ProdutoUpdate import ProdutoUpdate
from schemas.cliente.ClienteIn import ClienteIn
from schemas.cliente.Cliente import Cliente
from schemas.encomenda.EncomendaIn import EncomendaIn
from schemas.encomenda.EncomendaUpdate import EncomendaUpdate
from schemas.encomenda.EncomendaLocalizacao import EncomendaLocalizacao

def get_cliente(db: Session, cliente_id: int):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.cliente_id == cliente_id).first()

    if db_cliente is None:
        raise ValueError(f"Cliente com id {cliente_id} não encontrado.")
    
    return db_cliente

def get_cliente_by_cpf(db: Session, cpf: str):
    return db.query(models.Cliente).filter(models.Cliente.cpf == cpf).first()

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def get_clientes_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).filter(models.Cliente.status == status).offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: ClienteIn):
    db_cliente = models.Cliente(
        **cliente.model_dump(exclude=['password']), 
        hash_password=Cliente.hash_pswd(cliente.password)
    )
    
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def update_cliente(db: Session, cliente_id:int, clienteUpdate: ClienteIn):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.cliente_id == cliente_id).first()
    if clienteUpdate.nome is not None:
        db_cliente.nome = clienteUpdate.nome
    if clienteUpdate.email is not None:
        db_cliente.email = clienteUpdate.email
    if clienteUpdate.cpf is not None:
        db_cliente.cpf = clienteUpdate.cpf
    if clienteUpdate.telefone is not None:
        db_cliente.telefone = clienteUpdate.telefone
    if clienteUpdate.endereco is not None:
        db_cliente.endereco = clienteUpdate.endereco
    if clienteUpdate.password is not None:
        db_cliente.hash_password = Cliente.hash_pswd(clienteUpdate.password)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, cliente_id: int):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.cliente_id == cliente_id).first()
    db_cliente.status = 'INATIVO'
    db.commit()
    db.refresh(db_cliente)

def get_produto(db: Session, produto_id: int):
    prod = db.query(models.Produto).filter(models.Produto.produto_id == produto_id).first()
    if prod is None:
        raise ValueError(f"Produto de id {produto_id} não encontrado")
    return prod

def get_produto_by_nome(db: Session, nome: str):
    return db.query(models.Produto).filter(models.Produto.nome == nome).first()

def get_produtos(db: Session, skip: int = 0, limit: int = 100, min_price: float = 0.0, max_price: float = 1000000.0):
    return db.query(models.Produto).filter(models.Produto.preco >= min_price, models.Produto.preco <= max_price).offset(skip).limit(limit).all()

def create_produto(db: Session, produto: ProdutoIn):
    existe = get_produto_by_nome(db, produto.nome)
    if existe is not None:
        if existe.status != 'INATIVO':
            raise ValueError(f"Produto de nome {produto.nome} já existe.")
    
    db_produto = models.Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def update_produto(db: Session, produto_id:int, produtoUpdate: ProdutoUpdate):
    db_produto = db.query(models.Produto).filter(models.Produto.produto_id == produto_id).first()

    if db_produto is None:
        raise ValueError(f"Produto com id {produto_id} não encontrado.")

    if produtoUpdate.nome is not None:
        db_produto.nome = produtoUpdate.nome
    if produtoUpdate.preco is not None:
        db_produto.preco = produtoUpdate.preco
    if produtoUpdate.descricao is not None:
        db_produto.descricao = produtoUpdate.descricao
    db_produto.ultima_atualizacao = datetime.now()
    db.commit()
    db.refresh(db_produto)
    return db_produto

def delete_produto(db: Session, produto_id: int):
    db_produto = db.query(models.Produto).filter(models.Produto.produto_id == produto_id).first()

    if db_produto is None:
        raise ValueError(f"Produto com id {produto_id} não encontrado.")

    db_produto.status = 'INATIVO'

    db.commit()
    db.refresh(db_produto)


def get_encomenda(db: Session, encomenda_id: int):
    db_encomenda = db.query(models.Encomenda).filter(models.Encomenda.encomenda_id == encomenda_id).first()

    if db_encomenda is None:
        raise ValueError(f"Encomenda com id {encomenda_id} não encontrada.")
    
    return db_encomenda

def get_encomendas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Encomenda).offset(skip).limit(limit).all()

def get_encomendas_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    return db.query(models.Encomenda).filter(models.Encomenda.status == status).offset(skip).limit(limit).all()

def create_encomenda(db: Session, encomenda: EncomendaIn):
    db_encomenda = models.Encomenda(**encomenda.model_dump(exclude=['produtos', 'localizacaoAtual']))

    db_cliente = db.query(models.Cliente).filter(models.Cliente.cliente_id == encomenda.cliente_id).first()

    if db_cliente is None:
        raise ValueError(f"Cliente com id {encomenda.cliente_id} não encontrado.")

    valor_total = 0
    
    encomenda_produtos = []
    for produto_id, quantidade in encomenda.produtos.items():
        db_produto = db.query(models.Produto).filter((models.Produto.produto_id == int(produto_id)) & (models.Produto.status == "ATIVO")).first()
        
        if db_produto is None:
            raise ValueError(f"Produto com id {produto_id} não encontrado ou não é mais ativo.")
        
        valor_total += db_produto.preco * quantidade

        db_encomenda_produto = models.EncomendaProduto(encomenda_id=db_encomenda.encomenda_id, produto_id=produto_id, quantidade=quantidade)
        encomenda_produtos.append(db_encomenda_produto)
    
    db_encomenda.valor_total = valor_total

    db.add(db_encomenda)
    db.commit()
    db.refresh(db_encomenda)

    for encomenda_produto in encomenda_produtos:
        encomenda_produto.encomenda_id = db_encomenda.encomenda_id
        db.add(encomenda_produto)

    # Cria EncomendaLocalizacao
    db_localizacao = models.EncomendaLocalizacao(encomenda_id=db_encomenda.encomenda_id, localizacao=encomenda.localizacaoAtual)
    db.add(db_localizacao)
    db.commit()
    db.refresh(db_localizacao)

    db_encomenda.localizacao_atual_id = db_localizacao.localizacao_id
    
    db.add(db_encomenda)
    db.commit()
    db.refresh(db_encomenda)

    return db_encomenda

def update_encomenda(db: Session, encomenda_id: int, encomenda: EncomendaUpdate):
    db_encomenda = db.query(models.Encomenda).filter(models.Encomenda.encomenda_id == encomenda_id).first()

    if db_encomenda is None:
        raise ValueError(f"Encomenda com id {encomenda_id} não encontrada.")
    if encomenda.clienteId is not None:
        db_cliente = db.query(models.Cliente).filter(models.Cliente.cliente_id == encomenda.clienteId).first()
        if db_cliente is None:
            raise ValueError(f"Cliente com id {encomenda.clienteId} não encontrado.")
        db_encomenda.cliente_id = encomenda.clienteId
    if encomenda.descricao is not None:
        db_encomenda.descricao = encomenda.descricao
    if encomenda.produtos is not None:
        new_valor_total = 0
        old_produtos = db.query(models.EncomendaProduto).filter(models.EncomendaProduto.encomenda_id == encomenda_id).all()

        # Deleta os produtos antigos
        for old_produto in old_produtos:
            db.delete(old_produto)
        db.commit()

        new_encomenda_produto = []

        for produto_id, quantidade in encomenda.produtos.items():
            db_produto = db.query(models.Produto).filter(models.Produto.produto_id == int(produto_id)).first()
            
            if db_produto is None:
                raise ValueError(f"Produto com id {produto_id} não encontrado.")

            db_encomenda_produto = models.EncomendaProduto(encomenda_id=encomenda_id, produto_id=produto_id, quantidade=quantidade)
            new_encomenda_produto.append(db_encomenda_produto)
            new_valor_total += db_produto.preco * quantidade
        
        db_encomenda.valor_total = new_valor_total
        
        for new_produto in new_encomenda_produto:
            db.add(new_produto)

    if encomenda.localizacaoAtual is not None:
        db_localizacao = models.EncomendaLocalizacao(encomenda_id=encomenda_id, localizacao=encomenda.localizacaoAtual)
        db.add(db_localizacao)

        db.commit()
        db.refresh(db_localizacao)

        db_encomenda.localizacao_atual_id = db_localizacao.localizacao_id

    db.add(db_encomenda)
    db.commit()
    db.refresh(db_encomenda)

    return db_encomenda

def update_encomenda_status(db: Session, encomenda_id: int, status: str):
    db_encomenda = db.query(models.Encomenda).filter(models.Encomenda.encomenda_id == encomenda_id).first()
    if db_encomenda is None:
        raise ValueError(f"Encomenda com id {encomenda_id} não encontrada.")
    db_encomenda.status = status
    db.commit()
    db.refresh(db_encomenda)
    return db_encomenda

def delete_encomenda(db: Session, encomenda_id: int):
    db_encomenda = db.query(models.Encomenda).filter(models.Encomenda.encomenda_id == encomenda_id).first()

    if db_encomenda is None:
        raise ValueError(f"Encomenda com id {encomenda_id} não encontrada.")
    
    db_encomenda.localizacao_atual_id = None
    db.add(db_encomenda)
    db.commit()
    
    db_encomenda_produtos = db.query(models.EncomendaProduto).filter(models.EncomendaProduto.encomenda_id == encomenda_id).all()
    db_encomenda_localizacao = db.query(models.EncomendaLocalizacao).filter(models.EncomendaLocalizacao.encomenda_id == encomenda_id).all()

    for produto in db_encomenda_produtos:
        db.delete(produto)
    
    for localizacao in db_encomenda_localizacao:
        db.delete(localizacao)

    db.commit()

    db.delete(db_encomenda)
    db.commit()

def update_localizacao_encomenda(db: Session, localizacao: EncomendaLocalizacao):
    db_encomenda = db.query(models.Encomenda).filter(models.Encomenda.encomenda_id == localizacao.encomenda_id).first()
    
    if db_encomenda is None:
        raise ValueError(f"Encomenda com id {localizacao.encomenda_id} não encontrada.")
    
    db_localizacao = models.EncomendaLocalizacao(encomenda_id=localizacao.encomenda_id, localizacao=localizacao.localizacao)
    db.add(db_localizacao)
    db.commit()
    db.refresh(db_localizacao)
    
    db_encomenda.localizacao_atual_id = db_localizacao.localizacao_id

    db.commit()
    db.refresh(db_localizacao)
    db.refresh(db_encomenda)
    return db_encomenda

def get_encomenda_localizacao(db: Session, encomenda_id: int):
    localizacoes = db.query(models.EncomendaLocalizacao).filter(models.EncomendaLocalizacao.encomenda_id == encomenda_id).all()

    if not localizacoes:
        raise ValueError(f"Localizações da encomenda com id {encomenda_id} não encontradas.")

    return localizacoes


def get_encomenda_produtos(db: Session, encomenda_id: int):
    produtos = db.query(models.EncomendaProduto).filter(models.EncomendaProduto.encomenda_id == encomenda_id).all()

    if not produtos:
        raise ValueError(f"Produtos da encomenda com id {encomenda_id} não encontrados.")

    return produtos

def get_cliente_encomendas(db: Session, cliente_id: int):
    encomendas = db.query(models.Encomenda).filter(models.Encomenda.cliente_id == cliente_id).all()

    if not encomendas:
        raise ValueError(f"Encomendas do cliente com id {cliente_id} não encontradas.")

    return encomendas