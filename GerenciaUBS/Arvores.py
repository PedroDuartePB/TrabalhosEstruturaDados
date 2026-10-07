from __future__ import annotations
from typing import Optional


# Para encapsular o que for colocado aqui e gerar a chave_busca adequada
class No:
    def __init__(self, dado, chave_busca: int):
        self.paciente = dado
        self.chave_busca:int = chave_busca
        self.esquerda: Optional['No'] = None
        self.direita: Optional['No'] = None

    def get_dado(self):
        return self.paciente

    def __lt__(self, outro):
        return self.chave_busca < outro.chave_busca

    def __gt__(self, outro):
        return self.chave_busca > outro.chave_busca


class ArvoreBusca:
    def __init__(self):
        self.raiz: Optional[No] = None

    def is_empty(self) -> bool:
        return self.raiz is None

    def inserir(self, novo_dado, chave_busca: int):
        """Encapsula um dado qualqer recebido dentro de um novo nó e o insere na árvore."""
        if self.is_empty():
            self.raiz = No(novo_dado, chave_busca)
        else:
            atual = self.raiz
            while True:
                if chave_busca < atual.chave_busca:
                    if atual.esquerda is None:
                        atual.esquerda = No(novo_dado, chave_busca)
                        break
                    atual = atual.esquerda
                elif chave_busca > atual.chave_busca:
                    if atual.direita is None:
                        atual.direita = No(novo_dado, chave_busca)
                        break
                    atual = atual.direita
                else:
                    break

    def buscar(self, chave_busca: int) -> Optional[No]:
        """Percorre a árvore a partir da raiz até encontrar o nó que possui a chave passada. Retorna o nó com chave igual a passada ou None caso não consiga encontrar o nó requisitado."""
        atual = self.raiz
        while atual is not None:
            if chave_busca == atual.chave_busca:
                return atual
            elif chave_busca < atual.chave_busca:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def remover(self, cpf: int) -> Optional[No]:
        """Percorre a árvore de forma recursiva até encontrar o nó com a chave passada e o remove da árvore."""
        raiz, no_removido = self._remover_recursivo(cpf, self.raiz)
        return no_removido

    def _remover_recursivo(self, chave: int, raiz: Optional[No]) -> tuple[Optional[No], Optional[No]]:
        if raiz is None:
            return None, None

        if chave < raiz.chave_busca:
            raiz.esquerda, removido = self._remover_recursivo(chave, raiz.esquerda)
            return raiz, removido
        elif chave > raiz.chave_busca:
            raiz.direita, removido = self._remover_recursivo(chave, raiz.direita)
            return raiz, removido

        else:
            alvo_removido = No(raiz.paciente, raiz.chave_busca)

            if raiz.esquerda is None:
                return raiz.direita, alvo_removido
            elif raiz.direita is None:
                return raiz.esquerda, alvo_removido

            sucessor = raiz.direita
            while sucessor.esquerda is not None:
                sucessor = sucessor.esquerda

            raiz.paciente = sucessor.paciente
            raiz.chave_busca = sucessor.chave_busca

            raiz.direita, _ = self._remover_recursivo(sucessor.chave_busca, raiz.direita)

            return raiz, alvo_removido


class Heap:
    def __init__(self):
        self.heap:list[No] = []
        # 2*i+1 (esquerda), 2*(i+1) (direita), (i-1)//2 (pai)

    def _trocar_posicoes(self, i:int, j:int):
        self.heap[j], self.heap[i] = self.heap[i], self.heap[j]

    @staticmethod
    def _get_indice_pai(indice)->int:
        return (indice-1)//2

    @staticmethod
    def _heapify(lista:list[No], index: int):
        maior = index
        esquerda = 2 * index + 1
        direita = 2 * index + 2
        tamanho = len(lista)

        if esquerda < tamanho and lista[esquerda].chave_busca > lista[maior].chave_busca:
            maior = esquerda
        if direita < tamanho and lista[direita].chave_busca > lista[maior].chave_busca:
            maior = direita
        if maior != index:
            lista[index], lista[maior] = lista[maior], lista[index]
            Heap._heapify(lista, maior)

    def get_sorted_heap(self)->list[No]|None:
        if self.is_empty():
            return None
        else:
            heap:list[No] = self.heap.copy()
            ordenada: list[No] = []
            cauda = len(heap)
            self._heapify(heap, cauda)

            for i in range(cauda, 0, -1):
                heap[0], heap[i-1] = heap[i-1], heap[0]
                ordenada.append(heap.pop())
                self._heapify(heap, 0)

            return ordenada

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def get_topo(self):
        return self.heap[0]

    def inserir(self, dado: object, chave:int):
        novo_no = No(dado, chave)
        self.heap.append(novo_no)

        i = len(self.heap) - 1
        while i > 0:
            pai = self._get_indice_pai(i)
            if self.heap[i].chave_busca > self.heap[pai].chave_busca:
                self._trocar_posicoes(i, pai)
                i = pai
            else:
                break

    def remover(self):
        if self.is_empty():
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        topo = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify(self.heap, 0)
        return topo
