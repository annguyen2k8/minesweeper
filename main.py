# import keyboard
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from typing import Optional, Union

from game import *
from utils import *

def main():
    game = Minesweeper.init_from_level(Levels.BEGINER)
    focus = [0, 0]

    @show_latency
    def display():
        rows = [[" " for x in range(game.width)] for y in range(game.height)]

        def func(cell: Cell):
            char = cell.get_char()
            if cell.x == focus[0] and cell.y == focus[1]:
                char = char.replace(BG_GRAY, BG_WHITE)
            rows[cell.y][cell.x] = char

        game.foreach_cell(func)
        print("\x1b[2J\x1b[H\033[0")

        for row in rows:
            print("".join(row))
        print(game.mine_count, "mines")

    display()

    actives = []

    def on_press(key: Optional[Union[Key, KeyCode]]):
        if key not in actives:
            match key:
                case Key.up:
                    focus[1] -= 1
                case Key.down:
                    focus[1] += 1
                case Key.left:
                    focus[0] -= 1
                case Key.right:
                    focus[0] += 1

            char = getattr(key, "char", None)
            if char != None:
                match char:
                    case "q":
                        exit()
                    case "z":
                        game.open_at(*focus)
                    case "x":
                        game.flag_at(*focus)
            actives.append(key)

        focus[0] = clamp(0, focus[0], game.width - 1)
        focus[1] = clamp(0, focus[1], game.height - 1)

        display()

        if game.is_exploded or game.is_win:
            quit()

    def on_release(key: Optional[Union[Key, KeyCode]]):
        if key in actives:
            actives.remove(key)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
