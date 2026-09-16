from __future__ import annotations
import gc


class Paciente:
    cpf: int
    nome_completo: str
    cartao_sus: str
    tipo_atendimento: str

    def __init__(self, cpf, nome, cartao_sus, tipo_atendimento):
        self.cpf = cpf
        self.nome_completo = nome
        self.cartao_sus = cartao_sus
        self.tipo_atendimento = tipo_atendimento


class No:
    paciente: Paciente
    pai : No | None = None
    pont_esq: No | None = None
    pont_dir: No | None = None

    def __init__(self, paciente:Paciente):
        self.paciente = paciente


class Arvore:
    def __init__(self):
        self.Nos = []
        self.raiz = None

    def adicionar(self, paciente:Paciente):
        if self.raiz is None:
            self.raiz = No(paciente)
        else:
            atual = self.raiz
            pai = None

            while not atual is None:
                pai = atual

                if paciente.cpf > atual.paciente.cpf:
                    atual = atual.pont_dir
                elif paciente.cpf < atual.paciente.cpf:
                    atual = atual.pont_esq
                else:
                    raise CPFAlreadyInUseE("O cpf informado já está em uso")

            if paciente.cpf > pai.paciente.cpf:
                pai.pont_dir = No(paciente)
                pai.pont_dir.pai = pai
            elif paciente.cpf < pai.paciente.cpf:
                pai.pont_esq = No(paciente)
                pai.pont_dir.pai = pai



    def remover(self, chave:int):
        alvo = self.buscar(chave)
        pai = alvo.pai

        if chave > alvo.pai.paciente.cpf:
            pai.pont_dir = None
        elif chave < alvo.pai.paciente.cpf:
            pai.pont_esq = None

        delattr(alvo, 'pai')
        delattr(alvo, 'paciente')
        delattr(alvo, 'pont_dir')
        delattr(alvo, 'pont_esq')
        del alvo
        gc.collect()

    def buscar(self, chave:int)->No:
        atual = self.raiz

        while not atual is None and atual.paciente.cpf != chave:
            if chave > atual.paciente.cpf:
                atual = atual.pont_dir
            elif chave < atual.paciente.cpf:
                atual = atual.pont_esq

        return atual

class CPFAlreadyInUseE(Exception):
    def __init__(self, text):
        super.__init__(text)