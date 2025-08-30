import keyboard

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
        print('\x1b[2J\x1b[H\033[0')
       
        for row in rows:
            print("".join(row))
        print(game.mine_count, "mines")

    display()

    keys = {}
    while True:
        event = keyboard.read_event()
        key = event.name
        if key not in keys:
            keys[key] = keyboard.KEY_UP
        if event.event_type == keyboard.KEY_DOWN and keys[key] == keyboard.KEY_UP:
            match key:
                case "space":
                    game.open_at(*focus)
                case "z":
                    game.flag_at(*focus)
                case "up":
                    focus[1] -= 1
                case "down":
                    focus[1] += 1
                case "left":
                    focus[0] -= 1
                case "right":
                    focus[0] += 1
            focus[0] = clamp(0, focus[0], game.width - 1)
            focus[1] = clamp(0, focus[1], game.height - 1)
            
            display()
            
            if game.is_exploded or game.is_win:
                quit()
        keys[event.name] = event.event_type

if __name__ == "__main__":
    main()
