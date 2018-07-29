import copy
import math
import os
import time
from random import randint

from entidades import *


class Direcao(Enum):
    direita = 1
    esquerda = -1


class Jogo:

    def __init__(self):

        self.running = False
        self.jogador = None
        self.altura_mapa = 21
        self.largura_mapa = 79
        self.tela = []
        self.campo_batalha_limpo = []
        self.entidades = []
        self.campo_batalha_logico = []

        for i in range(0, self.altura_mapa + 1):
            self.tela.append(["X", "X"] + [" "] * self.largura_mapa)
            self.campo_batalha_logico.append([" "] * self.altura_mapa)

        self.campo_batalha_limpo = copy.deepcopy(self.tela)
        self.tela.append(["X"] * (self.largura_mapa + 2))

    def game_loop(self):
        cont = 0
        while True:
            if self.running:
                cont += 1
                self.update()
                self.draw()
                print('FRAME:', cont)
            time.sleep(.5)

    def start_game(self):
        self.running = True

        self.jogador = Jogador()
        self.entidades.append(self.jogador)
        self.jogador.y = self.altura_mapa // 2

        self.game_loop()

    def resume_game(self):
        self.running = True

    def pause_game(self):
        self.running = False

    def toggle_pause(self):
        if self.running:
            self.pause_game()
        else:
            self.resume_game()

    def mover_jogador_cima(self):
        if self.jogador.y > self.jogador.center[0]:
            self.jogador.y -= 1

    def mover_jogador_baixo(self):
        offset = len(self.jogador.corpo) - (self.jogador.center[0] + 1)
        if self.jogador.y < self.altura_mapa - offset:
            self.jogador.y += 1

    def limpar_tela(self):
        self.tela = copy.deepcopy(self.campo_batalha_limpo)

    def update(self):

        for e in self.entidades:
            if e.can_move_horizontally():
                e.x += 1 * e.direcao_horizontal.value
            # TODO mover verticalmente?

        for index, e in enumerate(self.entidades):
            for ee in self.entidades[index:]:

                if e is ee or e == ee:
                    continue

                posicoes_1 = e.get_coordenadas_ocupadas()
                posicoes_2 = ee.get_coordenadas_ocupadas()
                intersecao = set.intersection(posicoes_1, posicoes_2)
                print(posicoes_1, posicoes_2)
                print(e.y, e.x)
                print(ee.y, ee.x)
                print(intersecao)

                if len(intersecao) > 0:
                    print("colisao")
                    self.handle_collision(e, ee)

        self.enemy_generator()

    def enemy_generator(self):
        x = randint(1, 100)
        if x > 90:
            nave = Nave1(randint(1, self.altura_mapa - 5), self.largura_mapa - 2)
            self.entidades.append(nave)

    def atirar(self, entidade: Entidade):
        print('pew pew')
        tiro = Tiro(entidade)
        self.entidades.append(tiro)

    def handle_collision(self, entity1: Entidade, entity2: Entidade):
        print("colisao de {} com {}".format(entity1.__class__.__name__, entity2.__class__.__name__))

        if isinstance(entity2, Tiro):
            entity2, entity1 = entity1, entity2

        if isinstance(entity1, Tiro):
            if isinstance(entity2, Enemy):
                self.jogador.pontos += entity2.bounty
                self.entidades.remove(entity1)
                self.entidades.remove(entity2)

            elif isinstance(entity2, Tiro):
                self.entidades.remove(entity2)

            elif isinstance(entity2, Jogador):
                # TODO diminuir vida
                self.entidades.remove(entity1)

    def draw(self):

        os.system('clear')
        print(self.jogador.y)
        print("PONTOS:", self.jogador.pontos)

        self.limpar_tela()

        for e in self.entidades:
            try:
                self.draw_entity(e)
            except IndexError as error:
                if isinstance(e, Tiro):
                    self.entidades.remove(e)
                else:
                    raise error

        for i, linha in enumerate(self.tela):
            for ii, x in enumerate(linha):
                print(x, end="")
            print()

    def draw_entity(self, entidade: Entidade):

        posicao_y = math.floor(entidade.y)
        posicao_x = math.floor(entidade.x) + 2

        y = entidade.center[0]
        x = entidade.center[1]

        for index, linha in enumerate(entidade.corpo):
            for index2, xx in enumerate(linha):
                nova_posicao_y = posicao_y + (index - y)
                nova_posicao_x = posicao_x + (index2 - x)

                self.tela[nova_posicao_y][nova_posicao_x] = xx
