from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Paciente:
    cpf: int
    nome_completo: str
    cartao_sus: str
    tipo_atendimento: str


class No:
    #Só é preciso colocar atributos no init, deixar nos dois gera clones
    def __init__(self, paciente: Paciente, chave_busca:int):
        self.paciente = paciente
        # assim eu posso desacoplar o nó do paciente e até adaptar para outros objetos futuramente
        self.chave = chave_busca
        self.esquerda: Optional['No'] = None
        self.direita: Optional['No'] = None

    def has_children(self)->bool:
        if self.esquerda or self.direita:
            return True
        else:
            return False


class ArvorePacientes:
    def __init__(self, raiz = None):
        self.raiz: Optional[No] = raiz

    def is_empty(self) -> bool:
        return self.raiz is None

    def cadastrar_paciente(self, cpf: int, nome: str, cartao_sus: str, tipo_atendimento: str):
        novo_paciente = Paciente(cpf, nome, cartao_sus, tipo_atendimento)
        if self.is_empty():
            self.raiz = No(novo_paciente)

        atual = self.raiz
        while True:
            if cpf < atual.chave:
                if atual.esquerda is None:
                    atual.esquerda = No(novo_paciente)
                    break
                atual = atual.esquerda
            elif cpf > atual.chave:
                if atual.direita is None:
                    atual.direita = No(novo_paciente)
                    break
                atual = atual.direita
            else:
                break

    def buscar_paciente(self, cpf: int) -> Optional[Paciente]:
        #mudando para o modo recursivo pela simplicidade
        atual = self.raiz
        while atual is not None:
            if cpf == atual.chave:
                return atual.paciente
            elif cpf < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def remover_paciente(self, raiz:Optional[No], cpf: int)->Optional[No]:
        if raiz is None:
            return None

        if cpf < raiz.chave:
            raiz.esquerda = self.remover_paciente(raiz.esquerda, cpf)
        elif cpf > raiz.chave:
            raiz.direita = self.remover_paciente(raiz.direita, cpf)
        else:
            if raiz.esquerda is None:
                return raiz.direita
            elif raiz.direita is None:
                return raiz.esquerda

            sucessor = raiz.direita
            while sucessor.esquerda is not None:
                sucessor = sucessor.esquerda

            raiz.paciente = sucessor.paciente
            raiz.chave = sucessor.chave
            raiz.direita = self.remover_paciente(raiz.direita, sucessor.chave)

        return raiz

    def imprimir_atendimentos_dia(self, raiz: Optional[No]):
        if raiz is not None:
            print(f"Nome: {raiz.paciente.nome_completo} | CPF: {raiz.paciente.cpf}")
            self.imprimir_atendimentos_dia(raiz.esquerda)
            self.imprimir_atendimentos_dia(raiz.direita)

if __name__ == "__main__":
    arvore = ArvorePacientes()

    print("\n--- 1. Carga Inicial de Pacientes da UBS ---")
    pacientes = [
        (101, "Lucas Mendes", "SUS01", "Triagem"),
        (202, "Mariana Silva", "SUS02", "Vacinação"),
        (303, "Roberto Carlos", "SUS03", "Consulta"),
        (404, "Fernanda Lima", "SUS04", "Triagem"),
        (505, "João Pedro", "SUS05", "Vacinação"),
        (606, "Camila Alves", "SUS06", "Consulta")
    ]
    for p in pacientes:
        arvore.cadastrar_paciente(*p)
    print("6 pacientes cadastrados com sucesso.")

    print("\n--- 2. Remoção de Paciente ---")
    cpf_removido = 303
    arvore.raiz = arvore.remover_paciente(arvore.raiz, cpf_removido)
    print(f"Paciente com CPF {cpf_removido} removido por mudança de bairro.")

    print("\n--- 3. Simulação de Atendimento na Recepção ---")


    print("\n--- 4. Imprimir a agenda de atendimentos do dia ---")
    arvore.imprimir_atendimentos_dia(arvore.raiz)