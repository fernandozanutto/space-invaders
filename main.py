import time
import threading
from jogo import Jogo
from pynput import keyboard
from pynput.keyboard import Key


jogo = Jogo()


def start_game():
    cont = 0
    while True:
        cont += 1
        jogo.update()
        jogo.draw()
        print('FRAME:', cont)
        time.sleep(0.2)


def on_press(key):
    # print(key, 'foi pressionada')
    if key == Key.up:
        jogo.mover_jogador_cima()

    elif key == Key.down:
        jogo.mover_jogador_baixo()

    elif key == Key.space:
        jogo.atirar(jogo.jogador)


def on_release(key):
    pass


if __name__ == '__main__':
    t = threading.Thread(target=start_game)
    t.start()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
