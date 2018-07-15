import copy
import os
from entidades import *
from enum import Enum


class Direcao(Enum):
    direita = 1
    esquerda = -1


class Jogo:

    def __init__(self):
        self.jogador = None
        self.altura_mapa = 21
        self.largura_mapa = 79
        self.tela = []
        self.campo_batalha_limpo = []
        self.entidades = []

        for i in range(0, self.altura_mapa+1):
            self.tela.append(["X", "X"] + [" "] * self.largura_mapa)

        self.campo_batalha_limpo = copy.deepcopy(self.tela)
        self.tela.append(["X"] * (self.largura_mapa + 2))

        self.iniciar_jogo()

    def iniciar_jogo(self):
        self.jogador = Jogador()
        self.entidades.append(self.jogador)
        self.jogador.y = self.altura_mapa // 2

    def mover_jogador_cima(self):
        if self.jogador.y > self.jogador.center[0]:
            self.jogador.y -= 1

    def mover_jogador_baixo(self):
        offset = len(self.jogador.corpo) - (self.jogador.center[0]+1)
        if self.jogador.y < self.altura_mapa - offset:
            self.jogador.y += 1

    def limpar_tela(self):
        self.tela = copy.deepcopy(self.campo_batalha_limpo)

    def desenhar(self):
        os.system('clear')
        print(self.jogador.y)

        self.limpar_tela()
        for e in self.entidades:
            self.desenhar_entidade(e)

        for i in self.tela:
            for x in i:
                print(x, end="")
            print()

    def desenhar_entidade(self, entidade: Character):
        posicao_y = entidade.y
        posicao_x = entidade.x

        y = entidade.center[0]
        x = entidade.center[1]

        for index, linha in enumerate(entidade.corpo):
            for index2, xx in enumerate(linha):
                self.tela[posicao_y + (index-y)][posicao_x + (index2 - x)] = xx

    def update(self):
        for e in self.entidades:
            if e.can_move_horizontally():
                e.x += 1 * e.direcao_horizontal.value
            # TODO mover verticalmente?

    def atirar(self, entidade: Character):
        print('pew pew')
        tiro = Tiro(entidade)
        self.entidades.append(tiro)


