from dataclasses import dataclass
from enum import Enum

#Poderia fazer algo com isso para ajudar na prioriadde depois, atendimentos diferentes somam ou diminuem no valor prioridade
class TipoAtendimento(Enum):
    CONSULTA = -1
    VACINACAO = 1
    EMERGENCIA = 3

@dataclass
class Paciente:
    cpf: int
    nome_completo: str
    idade: int
    cartao_sus: str
    tipo_atendimento: TipoAtendimento

