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
    def __init__(self, paciente: Paciente, prioridade: int = 0):
        self.paciente = paciente
        self.esquerda: Optional['No'] = None
        self.direita: Optional['No'] = None
        self.pai: Optional['No'] = None
        self.prioridade: int = prioridade

    def has_children(self)->bool:
        if self.esquerda or self.direita:
            return True
        else:
            return False

    def get_prioridade(self)->int:
        return self.prioridade

    def set_prioridade(self, prioridade:int):
        self.prioridade = prioridade


class ArvorePacientes:
    def __init__(self, raiz = None):
        self.raiz: Optional[No] = raiz

    def is_empty(self) -> bool:
        return self.raiz is None

    def cadastrar_paciente(self, cpf: int, nome: str, cartao_sus: str, tipo_atendimento: str):
        novo_paciente = Paciente(cpf, nome, cartao_sus, tipo_atendimento)

        if self.is_empty():
            self.raiz = No(novo_paciente)
            print(f"Paciente {nome} cadastrado com sucesso na raiz.")
            return

        atual = self.raiz
        num_buscas = 0
        while True:
            if cpf < atual.paciente.cpf:
                if atual.esquerda is None:
                    atual.esquerda = No(novo_paciente, num_buscas)
                    print(f"Paciente {nome} cadastrado à esquerda de {atual.paciente.nome_completo}.")
                    break
                atual = atual.esquerda

            elif cpf > atual.paciente.cpf:
                if atual.direita is None:
                    atual.direita = No(novo_paciente, num_buscas)
                    print(f"Paciente {nome} cadastrado à direita de {atual.paciente.nome_completo}.")
                    break
                atual = atual.direita

            else:
                print(f"Aviso: O CPF {cpf} já está cadastrado. Inserção ignorada.")
                break

            num_buscas += 1

    def buscar_paciente(self, cpf: int) -> Optional[Paciente]:
        atual = self.raiz

        if self.is_empty():
            print(f"Paciente com CPF {cpf} não encontrado, árvore vazia.")
            return None

        while atual is not None:
            if cpf == atual.paciente.cpf:
                print("-" * 30)
                print(f"Paciente encontrado!")
                print(f"Dados: {atual.paciente}")
                print("-" * 30)
                return atual.paciente

            elif cpf < atual.paciente.cpf:
                atual = atual.esquerda
            else:
                atual = atual.direita

        print(f"Paciente com CPF {cpf} não cadastrado na triagem do dia.")
        return None

    def remover_paciente(self, cpf: int):
        alvo = self.raiz
        atual = self.raiz

        # Do While (improvisado devido a falta de suporte) para busca.
        while True:
            if atual is not None and atual.paciente.cpf < cpf:
                atual = atual.esquerda
            elif atual is not None and atual.paciente.cpf > cpf:
                atual = atual.direita
            elif atual is not None and atual.paciente.cpf == cpf:
                alvo = atual
                break
            else:
                return None

            alvo = atual

        # remoção de casos onde há 1 ou 2 filhos
        pai = alvo.pai
        if alvo.has_children():
            if alvo.esquerda is not None and alvo.direita is not None:
                pai_sucessor = alvo
                sucessor = alvo.direita

                while sucessor.esquerda is not None:
                    pai_sucessor = sucessor
                    sucessor = sucessor.esquerda

                alvo.paciente = sucessor.paciente


                alvo = sucessor
                pai = pai_sucessor


            filho_sobrevivente = alvo.esquerda if alvo.esquerda is not None else alvo.direita

            if pai is None:
                self.raiz = filho_sobrevivente
            elif pai.esquerda == alvo:
                pai.esquerda = filho_sobrevivente
            else:
                pai.direita = filho_sobrevivente

        #remoção de nó sem filhos
        else:
            if pai is None:
                self.raiz = None
            elif pai.esquerda == alvo:
                pai.esquerda = None
            else:
                pai.direita = None

    def enfileirar_atendimento(self):
        pass

    def listar_atendimentos_dia(self, no:No):
        saida:str = ""
        if no.esquerda is not None:
            saida += f"{self.listar_atendimentos_dia(no.esquerda)}"
        elif no.direita is not None:
            saida += f"{self.listar_atendimentos_dia(no.direita)}"

        saida += f"{no.paciente.nome_completo} - {no.paciente.cpf}\n"

        return saida
