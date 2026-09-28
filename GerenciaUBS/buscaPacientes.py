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

    def cadastrar_paciente(self, novo_paciente:Paciente, chave_alvo: Optional[int]=None):
        #paleativo até eu implementar a prioridade real
        if chave_alvo is None:
            chave_alvo = novo_paciente.cpf
        if self.is_empty():
            self.raiz = No(novo_paciente, chave_alvo)
            return
        else:
            atual = self.raiz
            while True:
                if novo_paciente.cpf < atual.chave:
                    if atual.esquerda is None:
                        atual.esquerda = No(novo_paciente, chave_alvo)
                        break
                    atual = atual.esquerda
                elif novo_paciente.cpf > atual.chave:
                    if atual.direita is None:
                        atual.direita = No(novo_paciente, chave_alvo)
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

    def remover_paciente(self, cpf: int, raiz: Optional[No]=None) -> Optional[No]:
        if raiz is None:
            return None

        if cpf < raiz.chave:
            raiz.esquerda = self.remover_paciente(cpf, raiz.esquerda)
        elif cpf > raiz.chave:
            raiz.direita = self.remover_paciente(cpf, raiz.direita)
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
            raiz.direita = self.remover_paciente(sucessor.chave, raiz.direita)

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
        raiz = self.db.raiz

        self.db.remover_paciente(cpf, raiz)

    def cadastro_novo(self, cpf: int, nome: str, cartao_sus: str, tipo_atendimento: str):
        self.db.cadastrar_paciente(Paciente(cpf, nome, cartao_sus, tipo_atendimento))

    def cadastro_buscar(self, cpf:int):
        return self.db.buscar_paciente(cpf).paciente

    def agendar_atendimento(self, cpf:int):
        cadastro = self.db.buscar_paciente(cpf)
        if cadastro is None:
            print("Paciente não encontrado, por favor realise o cadastro.")
        else:
            self.agenda.cadastrar_paciente(cadastro.paciente, )
            print(f"Cadastrado com sucesso: {cadastro.paciente}")

    def flush_agenda(self):
        if self.agenda.raiz is not None:
            self.agenda.remover_paciente(self.agenda.raiz.chave, self.agenda.raiz)

    def imprimir_atendimentos_dia(self, raiz: Optional[No]):
        if raiz is not None:
            print(f"Nome: {raiz.paciente.nome_completo} | CPF: {raiz.paciente.cpf}")
            self.imprimir_atendimentos_dia(raiz.esquerda)
            self.imprimir_atendimentos_dia(raiz.direita)

if __name__ == "__main__":
    db_paciente = GerenciardorPacientes()

    print("\n--- 1. Carga Inicial de Pacientes da UBS ---")
    pacientes = [(230, "jonas", "sus", "a"),
    (137, "marcia", "sus", "Triagem"),
    (112, "lucas", "sus", "Vacinação"),
    (504, "fulano", "sus", "Consulta"),
    (207, "jessica", "sus", "Triagem"),
    (150, "cassio", "sus", "Vacinação"),
    (101, "Lucas Mendes", "sus", "Triagem"),
    (202, "Mariana Silva", "sus", "Vacinação"),
    (303, "Roberto Carlos", "sus", "Consulta"),
    (404, "Fernanda Lima", "sus", "Triagem"),
    (505, "João Pedro", "sus", "Vacinação"),
    (606, "Camila Alves", "sus", "Consulta")]

    print(db_paciente.db.buscar_paciente(99))

    for i in pacientes:
        db_paciente.cadastro_novo(*i)

    print("6 pacientes cadastrados com sucesso.")

    for j in pacientes:
        print(db_paciente.db.buscar_paciente(int(j[0])))

    print(db_paciente.db.buscar_paciente(99))

    p7 = Paciente(112,"mariana", "sus", "a")


    print("\n--- 2. Remoção de Paciente ---")
    cpf_removido = 303
    db_paciente.db.raiz = db_paciente.cadastro_remover(cpf_removido)
    print(f"Paciente com CPF {cpf_removido} removido por mudança de bairro.")

    print("\n--- 3. Simulação de Atendimento na Recepção ---")


    print("\n--- 4. Imprimir a agenda de atendimentos do dia ---")
    db_paciente.imprimir_atendimentos_dia(db_paciente.agenda.raiz)