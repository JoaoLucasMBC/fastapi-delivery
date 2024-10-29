from enum import Enum

class EncomendaStatus(Enum):
    PENDENTE = "PENDENTE"
    EM_PREPARACAO = "EM_PREPARACAO"
    PRONTA = "PRONTA"
    ENTREGUE = "ENTREGUE"
    CANCELADA = "CANCELADA"