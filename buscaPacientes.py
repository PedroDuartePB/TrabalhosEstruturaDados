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

    def __str__(self) -> str:
        return f"{self.cpf}, {self.nome_completo}, {self.cartao_sus}, {self.tipo_atendimento}"


class No:
    paciente: Paciente
    pai : No | None = None
    pont_esq: No | None = None
    pont_dir: No | None = None

    def __init__(self, paciente:Paciente):
        self.paciente = paciente

    def has_children(self)->bool:
        if self.pont_esq or self.pont_dir:
            return True
        else:
            return False

class Arvore:
    def __init__(self):
        self.Nos = []
        self.raiz: No | None = None

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
            novo = No(paciente)
            if paciente.cpf > pai.paciente.cpf:
                pai.pont_dir = novo
                novo.pai = pai
            elif paciente.cpf < pai.paciente.cpf:
                pai.pont_esq = novo
                novo.pai = pai


    # função para remoção não testada
    def remover(self, chave:int):
        alvo = self.buscar(chave)
        if alvo is No:
            pai = alvo.pai

            if chave > pai.paciente.cpf:
                pai.pont_dir = None
            elif chave < pai.paciente.cpf:
                pai.pont_esq = None

            if not alvo.pont_esq is None:
                self.realocar_no(alvo.pont_esq)
            if not alvo.pont_dir is None:
                self.realocar_no(alvo.pont_dir)

            delattr(alvo, 'pai')
            delattr(alvo, 'paciente')
            delattr(alvo, 'pont_dir')
            delattr(alvo, 'pont_esq')
            del alvo
            gc.collect()

    def realocar_no(self, no:No):
        avo = no.pai.pai
        atual, cpf, prox = None, no.paciente.cpf,avo

        while not prox is None:
            atual = prox
            if atual.paciente.cpf < cpf:
                prox = atual.pont_dirs
            elif atual.paciente.cpf > cpf:
                prox = atual.pont_esq

        no.pai = atual
        if atual.paciente.cpf > cpf:
            atual.pont_esq = no
        else:
            atual.pont_dir = no

    def buscar(self, chave:int)->No|int:
        atual = self.raiz

        while not atual is None and atual.paciente.cpf != chave:
            if chave > atual.paciente.cpf:
                atual = atual.pont_dir
            elif chave < atual.paciente.cpf:
                atual = atual.pont_esq
        if atual is None:
            return -1
        return atual

class CPFAlreadyInUseE(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


if __name__ == "__main__":
    tree = Arvore()
    p1 = Paciente(20, "jonas", "sus", "a")
    p2 = Paciente(37, "marcia", "sus", "a")
    p3 = Paciente(12, "lucas", "sus", "a")
    p4 = Paciente(5, "fulano", "sus", "a")
    p5 = Paciente(27, "jessica", "sus", "a")
    p6 = Paciente(15, "cassio", "sus", "a")

    pacientes = [p1, p2, p3, p4, p5, p6]

    print(tree.buscar(99))

    for i in pacientes:
        tree.adicionar(i)

    for j in pacientes:
        print(tree.buscar(j.cpf).paciente)

    print(tree.buscar(99))

    p7 = Paciente( 12,"mariana", "sus", "a")
    try:
        tree.adicionar(p7)
    except CPFAlreadyInUseE as e:
        print(e)
