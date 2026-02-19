# Write your game here
import curses
import random
import time


class Game():
    def __init__(self):
        self.game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons
    'Board_Width' : 25,
    'Board_Height' : 15,
    'Obstacle' : [ {'x' : 5, 'y' : 7}, {'x' : 10, 'y' : 3}, {'x' : 15, 'y' : 10}, {'x' : 20, 'y' : 5}, {'x' : 8, 'y' : 12}, {'x' : 12, 'y' : 8}, {'x' : 18, 'y' : 2}, {'x' : 22, 'y' : 9} ],

    # Board pngs
    'obstacle': "\U0001FAA8 ",# 🪨
    'sword' : "\U0001f5e1\ufe0f", # 🗡️
    'axe' : "\U0001fa93", # 🪓
    'bow' : "\U0001f3f9", # 🏹
    'arrow' : "→", # →
    'empty': "  "
}
        self.player_data = {       
            'Player_Start' : {'x' : 5,'y' : 5},
            'Player_Health' : 5,
            'Player_Score' : 0,
            'Player_Icon' : "\U0001F9DD", # 🧝
 }
    
    def draw_board(self,stdscr):
    # Print the board and all game elements using curses
        stdscr.clear()
        for y in range(self.game_data["Board_Height"]):
            row = " "
            for x in range(self.game_data['Board_Width']):
                if self.player_data["Player_Start"]["x"] == x and self.player_data["Player_Start"]["y"] == y:
                    row += self.player_data['Player_Icon']
                elif any(o["x"] == x and o["y"] == y for o in self.game_data['Obstacle']):
                    row += self.game_data['obstacle']
                else:
                    row += self.game_data['empty']
            try:
                stdscr.addstr(y, 0, row, curses.color_pair(1))
            except curses.error:
                # Terminal may be too small for the board or unicode width; skip printing
                pass
        stdscr.refresh()
        # Wait for a keypress so the board remains visible until user presses a key
        while True:
            key = stdscr.getkey()
            if key.lower() == 'q':
                break
        stdscr.nodelay(False)
class Enemy():
    def __init__(self):
        self.enemy_data = {
}

# Good Luck!

adventure_game = Game()
# Use curses.wrapper with a callable that accepts the stdscr argument.
import sys, traceback

try:
    curses.wrapper(adventure_game.draw_board)
except Exception:
    try:
        curses.endwin()
    except Exception:
        pass
    traceback.print_exc()
    sys.exit(1)