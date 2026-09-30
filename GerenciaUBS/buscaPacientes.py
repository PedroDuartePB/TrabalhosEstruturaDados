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
        if self.raiz is None:
            return True
        else:
            return False

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

    def remover_paciente(self, cpf: int) -> Optional[No]:
        raiz, no_removido = self._remover_recursivo(cpf, self.raiz)
        return no_removido

    def _remover_recursivo(self, chave: int, raiz: Optional[No]) -> tuple[Optional[No], Optional[No]]:
        if raiz is None:
            return None, None

        if chave < raiz.chave:
            raiz.esquerda, removido = self._remover_recursivo(chave, raiz.esquerda)
            return raiz, removido
        elif chave > raiz.chave:
            raiz.direita, removido = self._remover_recursivo(chave, raiz.direita)
            return raiz, removido

        else:
            alvo_removido = No(raiz.paciente, raiz.chave)

            if raiz.esquerda is None:
                return raiz.direita, alvo_removido
            elif raiz.direita is None:
                return raiz.esquerda, alvo_removido

            sucessor = raiz.direita
            while sucessor.esquerda is not None:
                sucessor = sucessor.esquerda

            raiz.paciente = sucessor.paciente
            raiz.chave = sucessor.chave

            raiz.direita, _ = self._remover_recursivo(sucessor.chave, raiz.direita)

            return raiz, alvo_removido


class HeapAtendimento:
    def __init__(self):
        self.heap:list[No] = []
        self.cauda = 0

    def cadastrar_atendimento_dia(self, cpf: int, nome: str, cartao_sus: str, tipo_atendimento: str):
        pass


######################################################
# --- Grande fachada para melhor escrita de testes
######################################################

class GerenciardorPacientes:
    def __init__(self):
        self.db:ArvoreCadastros = ArvoreCadastros()
        self.agenda = HeapAtendimento()

    def cadastro_remover(self, cpf:int):
        raiz = self.db.raiz
        return self.db.remover_paciente(cpf).paciente

    def cadastro_novo(self, cpf: int, nome: str, cartao_sus: str, tipo_atendimento: str):
        self.db.cadastrar_paciente(Paciente(cpf, nome, cartao_sus, tipo_atendimento))

    def cadastro_buscar(self, cpf:int):
        cadastro = self.db.buscar_paciente(cpf)
        if cadastro is not None:
            return cadastro.paciente
        else:
            return None

    def agendar_atendimento(self, cpf:int):
        cadastro = self.cadastro_buscar(cpf)
        if cadastro is None:
            print(f"Recepção: CPF {cpf} não cadastrado na base da UBS.")
            return
        else:
            self.contador_chegada += 1
            self.agenda.cadastrar_paciente(cadastro, chave_alvo=self.contador_chegada)
            print(f"Recepção: {cadastro.nome_completo} chegou e foi enfileirado.")

    def finalizar_atendimento(self):
        if self.agenda.is_empty():
            print("Não há atendimentos agendados para o dia de hoje.")
        else:
            paciente_atendido = self.agenda.raiz
            while paciente_atendido.paciente.tipo_atendimento == "Concluído":
                paciente_atendido = paciente_atendido.direita
                if paciente_atendido is None:
                    print(f"Não restam mais atendimentos para serem realizados")
                    break
            paciente_atendido.paciente.tipo_atendimento = "Concluído"
            print("Atendimento concluído com sucesso.")

    def flush_agenda(self):
        if not self.agenda.is_empty():
            self.agenda.raiz = None

    def imprimir_atendimentos_dia(self, raiz: Optional[No]):
        if self.agenda.is_empty():
            print("Não há atendimentos agendados para o dia de hoje.")
        else:
            print(f"Nome: {raiz.paciente.nome_completo} | CPF: {raiz.paciente.cpf} | ATENDIMENTO {raiz.paciente.tipo_atendimento}")
            if raiz.esquerda is not None:
                self.imprimir_atendimentos_dia(raiz.esquerda)
            if raiz.direita is not None:
                self.imprimir_atendimentos_dia(raiz.direita)


if __name__ == "__main__":
    db_paciente = GerenciardorPacientes()

    input("Start: ")
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

    for i in pacientes:
        db_paciente.cadastro_novo(*i)

    print("6 pacientes cadastrados com sucesso.\n")

    for j in pacientes:
        print(db_paciente.cadastro_buscar(int(j[0])))

    input()
    print("\n--- 2. Remoção de Paciente ---")
    print(f"O paciente {db_paciente.cadastro_buscar(303).nome_completo} deseja mudar de UBS, remova o cadastro: ")
    cpf_removido = int(input("Qual cadastro deve ser removido? "))
    print(f"Paciente {db_paciente.cadastro_remover(cpf_removido).nome_completo} com CPF {cpf_removido} removido por mudança de bairro.")
    print(f"Busca do cpf removido: {db_paciente.cadastro_buscar(303)}")

    input()
    print("\n--- 3. Simulação de Atendimento na Recepção ---")

    cpfs_chegada = []
    for i in range(4):
        cpfs_chegada.append(int(input("Digite o cpf do paciente para agendar um atendimento: ")))
        db_paciente.agendar_atendimento(cpfs_chegada[i])

    input()
    print("Cadastro de paciente: ")
    db_paciente.cadastro_novo(int(input("Digite cpf do paciente: ")), input("Digite nome completo do paciente: "), input("Digite cartão do sus do paciente: "), input("Digite tipo de atendimento do paciente: "))
    db_paciente.agendar_atendimento(int(input("Digite o cpf do paciente para agendar um atendimento: ")))

    input()
    print("\n--- 4. Imprimir a agenda de atendimentos do dia ---")
    db_paciente.imprimir_atendimentos_dia(db_paciente.agenda.raiz)

    input("\nComeçar atendimento dos pacientes: ")
    db_paciente.finalizar_atendimento()
    db_paciente.imprimir_atendimentos_dia(db_paciente.agenda.raiz)

    input()
    print("Caso com agenda vazia: ")
    db_paciente.flush_agenda()
    db_paciente.imprimir_atendimentos_dia(db_paciente.agenda.raiz)
