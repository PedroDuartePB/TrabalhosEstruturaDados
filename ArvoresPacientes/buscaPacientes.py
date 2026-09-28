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
    def __init__(self, paciente: Paciente, chave_busca: int, prioridade:int=0):
        self.paciente = paciente
        self.chave:int = chave_busca
        self.prioridade:int = prioridade
        self.esquerda: Optional['No'] = None
        self.direita: Optional['No'] = None


class ArvoreCadastros:
    def __init__(self):
        self.raiz: Optional[No] = None

    def is_empty(self) -> bool:
        return self.raiz is None

    def cadastrar_paciente(self, novo_paciente:Paciente):
        if self.is_empty():
            self.raiz = No(novo_paciente, novo_paciente.cpf)
            return

        atual = self.raiz
        while True:
            if novo_paciente.cpf < atual.chave:
                if atual.esquerda is None:
                    atual.esquerda = No(novo_paciente, novo_paciente.cpf)
                    break
                atual = atual.esquerda
            elif novo_paciente.cpf > atual.chave:
                if atual.direita is None:
                    atual.direita = No(novo_paciente, novo_paciente.cpf)
                    break
                atual = atual.direita
            else:
                break

    def buscar_paciente(self, cpf: int) -> Optional[No]:
        atual = self.raiz
        while atual is not None:
            if cpf == atual.chave:
                return atual
            elif cpf < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None


    def remover_paciente(self, raiz: Optional[No], cpf: int) -> Optional[No]:
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

######################################################
# --- para a atividade de prioridade quando ela chegar
######################################################
#class HeapAtendimento:
#    def __init__(self):
#        self.heap:list[No] = []
#        self.cauda = 0


#    def cadastrar_atendimento_dia(self, cpf: int, nome: str, cartao_sus: str, tipo_atendimento: str):
#        pass

#    def imprimir_atendimentos_dia(self, raiz: Optional[No]):
#        if raiz is not None:
#            print(f"Nome: {raiz.paciente.nome_completo} | CPF: {raiz.paciente.cpf}")
#            self.imprimir_atendimentos_dia(raiz.esquerda)
#            self.imprimir_atendimentos_dia(raiz.direita)


######################################################
# --- Grande fachada para melhor escrita de testes
######################################################

class GerenciardorPacientes:
    def __init__(self):
        self.db:ArvoreCadastros = ArvoreCadastros()
        self.agenda = ArvoreCadastros()
        #self.agenda = HeapAtendimento()

    def cadastro_remover(self, cpf:int):
        alvo:No = self.db.buscar_paciente(cpf)
        self.db.remover_paciente(alvo, cpf)

    def cadastro_novo(self, cpf: int, nome: str, cartao_sus: str, tipo_atendimento: str):
        self.db.cadastrar_paciente(Paciente(cpf, nome, cartao_sus, tipo_atendimento))

    def cadastro_buscar(self, cpf:int):
        return self.db.buscar_paciente(cpf).paciente

    def agendar_atendimento(self, cpf:int):
        cadastro = self.db.buscar_paciente(cpf)
        if cadastro is None:
            print("Paciente não encontrado, por favor realise o cadastro.")
        else:
            self.agenda.cadastrar_paciente(cadastro.paciente)
            print(f"Cadastrado com sucesso: {cadastro.paciente}")

    def flush_agenda(self):
        self.agenda.remover_paciente(self.agenda.raiz, self.agenda.raiz.chave)

    def imprimir_atendimentos_dia(self, raiz: Optional[No]):
        if raiz is not None:
            print(f"Nome: {raiz.paciente.nome_completo} | CPF: {raiz.paciente.cpf}")
            self.imprimir_atendimentos_dia(raiz.esquerda)
            self.imprimir_atendimentos_dia(raiz.direita)

if __name__ == "__main__":
    db_paciente = GerenciardorPacientes()

    p1 = Paciente(20, "jonas", "sus", "a")
    p2 = Paciente(37, "marcia", "sus", "a")
    p3 = Paciente(12, "lucas", "sus", "a")
    p4 = Paciente(5, "fulano", "sus", "a")
    p5 = Paciente(27, "jessica", "sus", "a")
    p6 = Paciente(15, "cassio", "sus", "a")

    pacientes = [p1, p2, p3, p4, p5, p6]

    print(db_paciente.db.buscar_paciente(99))

    for i in pacientes:
        db_paciente.cadastro_novo(i.cpf, i.nome_completo, i.cartao_sus, i.tipo_atendimento)

    for j in pacientes:
        print(db_paciente.db.buscar_paciente(j.cpf))

    print(db_paciente.db.buscar_paciente(99))

    p7 = Paciente( 12,"mariana", "sus", "a")
