from enum import Enum


class Entidade:

    class DirecaoHorizontal(Enum):
        esquerda = -1
        direita = 1

    def __init__(self, direcao: DirecaoHorizontal):
        self.y = None
        self.x = None
        self.direcao_horizontal = direcao

    def can_move_horizontally(self):
        raise NotImplementedError("implementa o método na classe filho aí por favor")

    def can_move_vertically(self):
        raise NotImplementedError("implementa o método na classe filho aí por favor")


class Character(Entidade):
    def __init__(self, direcao: Entidade.DirecaoHorizontal):
        Entidade.__init__(self, direcao)
        self.corpo = None
        self.center = None


class Jogador(Character):
    def __init__(self):
        Character.__init__(self, Entidade.DirecaoHorizontal.direita)
        self.nome = input("Digite seu nome: ")
        self.x = 3 #jogador sempre fica no 3

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


class Nave1(Character):

    def __init__(self):
        Character.__init__(self, Entidade.DirecaoHorizontal.esquerda)

        self.corpo = [
            [' ', ' ', '*'],
            ['*', '*', '*'],
            [' ', '*', '*'],
            ['*', '*', '*'],
            [' ', ' ', '*'],
        ]

    def can_move_horizontally(self):
        return True

    def can_move_vertically(self):
        return False


class Tiro(Entidade):

    def __init__(self, dono: Character):
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
