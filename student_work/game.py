# Write your game here
import curses
import random
import time

class Game():
    def __init__(self):
        self.game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons
    'Board_Width' : 10,
    'Board_Height' : 10,
    'Obstacle' : [ {'x' : random.randint(10), 'y' : random.randint(10)},

    ],

    # Board pngs
    'obstacle': "\U0001FAA8 ",# 🪨
    'sword' : "\U0001f5e1\ufe0f", # 🗡️
    'axe' : "\U0001fa93", # 🪓
    'bow' : "\U0001f3f9", # 🏹
    'empty': "  "
}
        self.player_data = {       
            'Player_Start' : (5,5),
            'Player_Health' : 5,
 }
    
    def draw_board(self,stdsrc):
    # Print the board and all game elements using curses
        stdsrc.clear
        for y in range(self.game_data["Board_Height"]):
            row = " "
            for x in range(self.game_data["Board_Width"]):
                pass

class Enemy():
    def __init__(self):
        self.enemy_data = {
}

# Good Luck!