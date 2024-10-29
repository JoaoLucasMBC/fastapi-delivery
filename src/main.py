from typing import Optional, Annotated

from fastapi import FastAPI, HTTPException, status, Body, Depends

from schemas.produto.Produto import Produto
from schemas.produto.ProdutoIn import ProdutoIn
from schemas.produto.ProdutoUpdate import ProdutoUpdate

from schemas.encomenda.Encomenda import Encomenda
from schemas.encomenda.EncomendaIn import EncomendaIn
from schemas.encomenda.EncomendaHasProduto import EncomendaHasProduto
from schemas.encomenda.EncomendaLocalizacao import EncomendaLocalizacao
from schemas.encomenda.EncomendaStatus import EncomendaStatus
from schemas.encomenda.EncomendaUpdate import EncomendaUpdate

from schemas.cliente.Cliente import Cliente
from schemas.cliente.ClienteIn import ClienteIn
from schemas.cliente.ClienteUpdate import ClienteUpdate
from schemas.cliente.ClienteStatus import ClienteStatus

import crud, models
from database import SessionLocal, engine

from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


description = """
EJ Encomendas é seu app perfeito de encomendas!. 🚀

## Encomendas

Você poderá:

* **Criar encomendas**.    
* **Ler encomendas**.  
* **Atualizar status de encomendas**.  
* **Atualizar localização de encomendas**.  
* **Listar localizações de encomendas**.  
* **Listar produtos de encomendas**.  

## Produtos

Você poderá:

* **Criar produtos**.  
* **Ler produtos**.  
* **Atualizar produtos**.  
* **Deletar produtos**.  

## Clientes

Você poderá:

* **Criar clientes**.  
* **Ler clientes**.  
* **Atualizar clientes**.  
* **Deletar clientes**.  
"""

tags_metadata = [
    {
        "name": "Encomendas",
        "description": "Operações com encomendas. 📦",
    },
    {
        "name": "Produtos",
        "description": "Operações com produtos. 📦",
    },
    {
        "name": "Clientes",
        "description": "Operações com clientes. 📦",
    }
]

app = FastAPI(
    title="EJ Encomendas",
    description=description,
    summary="We ballin, Mr. Maciel",
    version="0.0.1",
    contact={
        "name": "EJ Encomendas",
        "email": "joaolmbc@al.insper.edu.br",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


# ROTAS DE ENCOMENDA
@app.get("/encomendas/", tags=["Encomendas"], response_model=list[Encomenda])
def read_encomendas(status: Optional[Annotated[EncomendaStatus, "status"]] = None, db:Session = Depends(get_db)):
    """
    Retorna todas as encomendas.

    Query Params:

        status (EncomendaStatus): Filtra as encomendas por status.
    """
    if status:
        return crud.get_encomendas_by_status(db, status.value)
    return crud.get_encomendas(db)

@app.get("/encomendas/{encomendaId}", tags=["Encomendas"], response_model=Encomenda)
def read_encomenda(encomendaId: int, db:Session = Depends(get_db)):
    """
    Retorna uma encomenda a partir de seu id.

    Path Params:

        encomendaId (int): Id da encomenda.
    """
    try:
        return crud.get_encomenda(db, encomendaId)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@app.post("/encomendas/", status_code=status.HTTP_201_CREATED, tags=["Encomendas"], response_model=Encomenda)
def create_encomenda(encomendaIn: EncomendaIn, db:Session = Depends(get_db)):
    """
    Cria uma nova encomenda, suas relações com produtos e localizações e a insere no banco de dados.

    Body:

        encomendaIn (EncomendaIn): Dados da encomenda.
    """

    try:
        return crud.create_encomenda(db, encomendaIn)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@app.put("/encomendas/{encomendaId}/status", status_code=status.HTTP_201_CREATED, tags=["Encomendas"], response_model=Encomenda)
def update_encomenda_status(encomendaId: int, status: EncomendaStatus = Body(embed=True), db: Session = Depends(get_db)):
    """
    Atualiza o status de uma encomenda.

    Path Params:

        encomendaId (int): Id da encomenda.
    
    Body:

        status (EncomendaStatus): Novo status da encomenda.
    """
    try:
        return crud.update_encomenda_status(db, encomendaId, status.value)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"Encomenda de id {encomendaId} não encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@app.put("/encomendas/{encomendaId}", status_code=status.HTTP_201_CREATED, tags=["Encomendas"], response_model=Encomenda)
def update_encomenda(encomendaId: int, encomendaUpdate: EncomendaUpdate, db: Session = Depends(get_db)):
    """
    Atualiza uma encomenda a partir de seu id.

    Path Params:

        encomendaId (int): Id da encomenda.
    
    Body:

        encomendaUpdate (EncomendaUpdate): Dados da encomenda a serem atualizados.
    """
    try:
        return crud.update_encomenda(db, encomendaId, encomendaUpdate)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@app.post("/encomendas/localizacao", status_code=status.HTTP_201_CREATED, tags=["Encomendas"], response_model=Encomenda)
def update_localizacao(localizacao: EncomendaLocalizacao, db: Session = Depends(get_db)):
    """
    Atualiza a localização de uma encomenda, que contém o id e a nova localização no histórico.

    Body:

        localizacao (EncomendaLocalizacao): Dados da localização.
    """
    try:
        return crud.update_localizacao_encomenda(db, localizacao)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@app.delete("/encomendas/{encomendaId}", status_code=status.HTTP_204_NO_CONTENT, tags=["Encomendas"])
def delete_encomenda(encomendaId: int, db: Session = Depends(get_db)):
    """
    Deleta uma encomenda a partir de seu id.

    Path Params:

        encomendaId (int): Id da encomenda.
    """
    try:
        crud.delete_encomenda(db, encomendaId)
        return
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@app.get("/encomendas/{encomendaId}/localizacao", tags=["Encomendas"], response_model=list[EncomendaLocalizacao])
def read_encomenda_localizacoes(encomendaId: int, db: Session = Depends(get_db)):
    """
    Lista todas as localizações de uma encomenda.

    Path Params:

        encomendaId (int): Id da encomenda.
    """
    try:
        return crud.get_encomenda_localizacao(db, encomendaId)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@app.get("/encomendas/{encomendaId}/produtos", tags=["Encomendas", "Produtos"], response_model=list[EncomendaHasProduto])
def read_encomenda_produtos(encomendaId: int, db: Session = Depends(get_db)):
    """
    Lista todos os produtos de uma encomenda.

    Path Params:

        encomendaId (int): Id da encomenda.
    """
    try:
        return crud.get_encomenda_produtos(db, encomendaId)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

# ROTAS DE PRODUTO
@app.get("/produtos/", tags=["Produtos"], response_model=list[Produto])
def read_produtos(min_price: Optional[float] = None, max_price: Optional[float] = None, db: Session = Depends(get_db)):
    """
    Lista todos os produtos, podendo filtrar por preço mínimo e máximo.

    Query Params:

        min_price (float): Preço mínimo do produto.

        max_price (float): Preço máximo do produto.
    """
    if min_price and max_price:
        return crud.get_produtos(db, min_price=min_price, max_price=max_price)
    elif min_price:
        return crud.get_produtos(db, min_price=min_price)
    elif max_price:
        return crud.get_produtos(db, max_price=max_price)
    return crud.get_produtos(db)

@app.get("/produtos/{produto_id}", tags=["Produtos"], response_model=Produto)
def read_produto(produto_id: int, db: Session = Depends(get_db)):
    '''
    Encontra um produto a partir de seu id.

    Path Params:

        produtoId (int): Id do produto.
    '''
    try:
        produto = crud.get_produto(db, produto_id)
        return produto 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produto de id {produto_id}: {e}")

@app.post("/produtos/", status_code=status.HTTP_201_CREATED, tags=["Produtos"], response_model=Produto)
def create_produto(produtoIn: ProdutoIn, db: Session = Depends(get_db)):
    '''
    Cria um novo produto e o insere no banco de dados.

    Body:

        produtoIn (ProdutoIn): Dados do produto.
    '''
    try:
        return crud.create_produto(db, produtoIn)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {e}")

@app.put("/produtos/{produtoId}", status_code=status.HTTP_201_CREATED, tags=["Produtos"], response_model=Produto)
def update_produto(produtoId: int, produtoIn: ProdutoUpdate, db: Session = Depends(get_db)):
    '''
    Atualiza um produto a partir de seu id.

    Path Params:

        produtoId (int): Id do produto.
    
    Body:

        produtoIn (ProdutoUpdate): Dados do produto a serem atualizados.
    '''
    try:
        produto = crud.update_produto(db, produtoId, produtoIn)
        return produto
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar produto de id {produtoId}: {e}")
    
@app.delete("/produtos/{produtoId}", status_code=status.HTTP_204_NO_CONTENT, tags=["Produtos"])
def delete_produto(produtoId: int, db: Session = Depends(get_db)):
    '''
    Deleta um produto a partir de seu id.

    Path Params:

        produtoId (int): Id do produto.
    '''
    try:
        crud.delete_produto(db, produtoId)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar produto de id {produtoId}: {e}")


# ROTAS DE CLIENTES
@app.get("/clientes/", tags=["Clientes"], response_model=list[Cliente])
def read_clientes(status: Optional[Annotated[ClienteStatus, "status"]] = None, db: Session = Depends(get_db)):
    '''
    Lista todos os clientes, podendo filtrar por status.

    Query Params:

        status (ClienteStatus): Filtra os clientes por status.
    '''
    try:
        if status:
            return crud.get_clientes_by_status(db, status.value)
        return crud.get_clientes(db)
    except:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar clientes")

@app.get("/clientes/{clienteId}", tags=["Clientes"], response_model=Cliente)
def read_cliente(clienteId: int, db: Session = Depends(get_db)):
    '''
    Lista um cliente a partir de seu id.

    Path Params:

        clienteId (int): Id do cliente.
    '''
    try:
        return crud.get_cliente(db, clienteId)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar cliente de id {clienteId}")

@app.post("/clientes/", status_code=status.HTTP_201_CREATED, tags=["Clientes"], response_model=Cliente)
def create_cliente(clienteIn: ClienteIn, db: Session = Depends(get_db)):
    '''
    Cria um novo cliente e o insere no banco de dados.

    Body:

        clienteIn (ClienteIn): Dados do cliente.
    '''
    try:
        if crud.get_cliente_by_cpf(db, clienteIn.cpf):
            raise HTTPException(status_code=400, detail=f"Cliente com CPF {clienteIn.cpf} já existe")

        return crud.create_cliente(db, clienteIn)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar cliente: {e}")

@app.put("/clientes/{clienteId}", status_code=status.HTTP_201_CREATED, tags=["Clientes"], response_model=Cliente)
def update_cliente(clienteId: int, clienteUpdate: ClienteUpdate, db: Session = Depends(get_db)):
    '''
    Atualiza um cliente a partir de seu id.

    Path Params:

        clienteId (int): Id do cliente.
    
    Body:  

        clienteUpdate (ClienteUpdate): Dados do cliente a serem atualizados.
    '''
    try:
        if crud.get_cliente(db, clienteId) is None:
            raise HTTPException(status_code=404, detail=f"Cliente de id {clienteId} não encontrado")
        cliente = crud.update_cliente(db, clienteId, clienteUpdate)
        return cliente
    except:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente de id {clienteId}")

@app.delete("/clientes/{clienteId}", status_code=status.HTTP_204_NO_CONTENT, tags=["Clientes"])
def delete_cliente(clienteId: int, db:Session = Depends(get_db)):
    '''
    Faz a deleção lógica de um cliente a partir de seu id.

    Path Params:

        clienteId (int): Id do cliente.
    '''
    try:
        if crud.get_cliente(db, clienteId) is None:
            raise HTTPException(status_code=404, detail=f"Cliente de id {clienteId} não encontrado")
        crud.delete_cliente(db, clienteId)
    except:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar cliente de id {clienteId}")

@app.get("/clientes/{clienteId}/encomendas/", tags=["Clientes", "Encomendas"], response_model=list[Encomenda])
def read_cliente_encomendas(clienteId: int, db: Session = Depends(get_db)):
    '''
    Lista todas as encomendas de um cliente.

    Path Params:

        clienteId (int): Id do cliente.
    '''
    try:
        return crud.get_cliente_encomendas(db, clienteId)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar encomendas do cliente de id {clienteId}: {e}")