import java.util.ArrayList;

public abstract class Arvore {
    ArrayList<No> nos;
    No raiz;

    public Arvore(){
        ArrayList<No> nos = new ArrayList<No>();
        No raiz = null;
    }

    public void adicionarNo(No novo){
        if (raiz == null){
            raiz = novo;
        } else {
            No atual = self.raiz;
            pai = null;

            do {
                pai = atual;
                if (paciente.cpf > atual.paciente.cpf){
                    atual = atual.pont_dir;
                }else if(paciente.cpf < atual.paciente.cpf){
                    atual = atual.pont_esq;
                }else{
                    throw IllegalArgumentException();
                }
                novo = No(paciente)
                if paciente.cpf > pai.paciente.cpf:
                pai.pont_dir = novo
                novo.pai = pai
                elif paciente.cpf < pai.paciente.cpf:
                pai.pont_esq = novo
                novo.pai = pai
            } while (atual != null);


    public No buscarNo(){
        No avo = no.pai.pai
        atual, cpf, prox = null, no.paciente.cpf,avo

        while not prox is null:
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

        while not atual is null and atual.paciente.cpf != chave:
        if chave > atual.paciente.cpf:
        atual = atual.pont_dir
        elif chave < atual.paciente.cpf:
        atual = atual.pont_esq

        return atual;
    }

}

class No{
    paciente: Paciente
    pai : No | null = null
    pont_esq: No | null = null
    pont_dir: No | null = null

    def __init__(self, paciente:Paciente):
    self.paciente = paciente

    def has_children(self)->bool:
            if self.pont_esq or self.pont_dir:
            return True
        else:
                return False
}

class Paciente {
    cpf:int
    nome_completo:str
    cartao_sus:str
    tipo_atendimento:str

    def __init__(self, cpf, nome, cartao_sus, tipo_atendimento):
    self.cpf =cpf
    self.nome_completo =nome
    self.cartao_sus =cartao_sus
    self.tipo_atendimento =tipo_atendimento

    def __str__(self) ->str:
            return f"{self.cpf}, {self.nome_completo}, {self.cartao_sus}, {self.tipo_atendimento}"
}
