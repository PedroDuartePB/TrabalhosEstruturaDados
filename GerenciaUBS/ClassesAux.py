from dataclasses import dataclass
from enum import Enum


class TipoAtendimento(Enum):
    VACINACAO = 0

@dataclass
class Paciente:
    cpf: int
    nome_completo: str
    idade: int
    cartao_sus: str
    tipo_atendimento: TipoAtendimento

