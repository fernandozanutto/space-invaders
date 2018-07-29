from enum import Enum


class Entidade:
    class DirecaoHorizontal(Enum):
        esquerda = -1
        direita = 1

    def __init__(self, direcao: DirecaoHorizontal):
        self.y = None
        self.x = None
        self.direcao_horizontal = direcao
        self.corpo = []
        self.center = None

    def can_move_horizontally(self):
        raise NotImplementedError("implementa o método na classe filho aí por favor")

    def can_move_vertically(self):
        raise NotImplementedError("implementa o método na classe filho aí por favor")

    def get_coordenadas_ocupadas(self):
        retorno = set()

        center_y = self.center[0]
        center_x = self.center[1]

        for y, linha in enumerate(self.corpo):
            for x, i in enumerate(linha):
                if i != ' ':
                    retorno.add((self.y + (y - center_y), self.x + (x - center_x)))

        return retorno


class Jogador(Entidade):
    def __init__(self):
        Entidade.__init__(self, Entidade.DirecaoHorizontal.direita)
        self.nome = input("Digite seu nome: ")
        self.x = 3  # jogador sempre fica no 3
        self.pontos = 0

        self.corpo = [
            ['+', ' '],
            ['+', '+'],
            ['+', ' ']
        ]

        self.center = (1, 0)

    def can_move_horizontally(self):
        return False

    def can_move_vertically(self):
        return True

    def __str__(self):
        return '+'


class Enemy(Entidade):
    def __init__(self):
        Entidade.__init__(self, Entidade.DirecaoHorizontal.esquerda)
        self.bounty = None


class Nave1(Enemy):

    def __init__(self, y, x):
        Enemy.__init__(self)

        self.x = x
        self.y = y
        self.corpo = [
            [' ', ' ', '*'],
            ['*', '*', '*'],
            [' ', '*', '*'],
            ['*', '*', '*'],
            [' ', ' ', '*'],
        ]
        self.center = (2, 2)
        self.bounty = 100

    def can_move_horizontally(self):
        return True

    def can_move_vertically(self):
        return False

    def __str__(self):
        return '*'


class Tiro(Entidade):

    def __init__(self, dono: Entidade):
        Entidade.__init__(self, dono.direcao_horizontal)
        self.dono = dono

        self.corpo = [['-']]
        self.center = (0, 0)
        self.y = dono.y
        self.x = dono.x + (1 * dono.direcao_horizontal.value)

    def can_move_vertically(self):
        return False

    def can_move_horizontally(self):
        return True

    def __str__(self):
        return '-'
