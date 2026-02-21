# Write your game here
import curses
import random


class Game():
    def __init__(self):
        self.game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons
    'Board_Width' : 25,
    'Board_Height' : 20,
    'Obstacle' : [{'x' : 5, 'y' : 7}, 
                  {'x' : 10, 'y' : 3}, 
                  {'x' : 15, 'y' : 10}, 
                  {'x' : 20, 'y' : 5}, 
                  {'x' : 8, 'y' : 12}, 
                  {'x' : 12, 'y' : 8}, 
                  {'x' : 18, 'y' : 2}, 
                  {'x' : 22, 'y' : 9},
                  {'x' : 3, 'y' : 4}, 
                  {'x' : 7, 'y' : 6},
                  {'x' : 14, 'y' : 14},
                  {'x' : 19, 'y' : 1},
                  {'x' : 2, 'y' : 20},
                  {'x' : 6, 'y' : 18},
                  {'x' : 11, 'y' : 13},
                  {'x' : 17, 'y' : 19},
                  {'x' : 21, 'y' : 17},
                  {'x' : 4, 'y' : 16},],

    'Enemy' : [{'x': 5, 'y': 5, 'icon': "\U0001F9DF"}, # 🧟
                {'x': 15, 'y': 15, 'icon': "\U0001F480"}], # 💀

    # Board pngs
    'obstacle': "\U0001FAA8 ",# 🪨
    'sword' : "\U0001F5E1", # 🗡️
    'empty': "  ",
    'skeleton' : "\U0001F480", # 💀
    'zombie': "\U0001F9DF", # 🧟  
    }


        self.player_data = {       
            'Player_Start' : {'x' : 2,'y' : 10},
            'Weapon_Start' : {'x' : 3, 'y' : 10},
            'Player_Health' : 5,
            'Player_Score' : 0,
            'Player_Icon' : "\U0001F9DD", # 🧝
            'Player_Weapon' : 'bow',
            }
    
        self.enemy_count = 2

    def draw_board(self,stdscr):
    # Print the board and all game elements using curses
        stdscr.clear()
        for y in range(self.game_data["Board_Height"]):
            row = " "
            for x in range(self.game_data['Board_Width']):
                if self.player_data["Player_Start"]["x"] == x and self.player_data["Player_Start"]["y"] == y:
                    row += self.player_data['Player_Icon']
                # elif self.player_data["Weapon_Start"]["x"] == x and self.player_data["Weapon_Start"]["y"] == y:
                #     row += self.game_data[self.player_data['Player_Weapon']]
                elif any(o["x"] == x and o["y"] == y for o in self.game_data['Obstacle']):
                    row += self.game_data['obstacle']
                elif any(e["x"] == x and e["y"] == y for e in self.game_data['Enemy']):
                    enemy = next(e for e in self.game_data['Enemy'] if e["x"] == x and e["y"] == y)
                    row += enemy['icon']
                else:
                    row += self.game_data['empty']
                try:
                    stdscr.addstr(y, 0, row, curses.color_pair(1))
                except curses.error:
                    pass
            
        try: 
            stdscr.addstr(self.game_data["Board_Height"] + 1, 20, f"Score: {self.player_data['Player_Score']} ")
            stdscr.addstr(self.game_data["Board_Height"] + 2, 1, "Move with W/A/S/D, Press G to attack, Q to quit")    
            stdscr.addstr(self.game_data["Board_Height"] + 1, 1, f"Health: {self.player_data['Player_Health']} ")
        except curses.error:
            # My code is being weird and sometimes throws an error when trying to print the score/health. This is a workaround to prevent it from crashing.
            pass  
        stdscr.refresh()    

    def move_player(self, direction):
        # Update player position based on input direction, ensuring they stay within bounds and avoid obstacles
        new_x = self.player_data["Player_Start"]["x"]
        new_y = self.player_data["Player_Start"]["y"]
        if direction == 'w':  # Up
            new_y -= 1    
        elif direction == 's':  # Down
            new_y += 1
        elif direction == 'a':  # Left
            new_x -= 1
        elif direction == 'd':  # Right
            new_x += 1
        elif direction == 'g':
            self.attack_enemy()
            return
        # Check for boundaries
        if self.check_obstacle_collision(new_x, new_y) == False:
            self.player_data["Player_Start"]["x"] = new_x
            self.player_data["Player_Start"]["y"] = new_y
            self.check_enemy_collision(new_x, new_y)


    def attack_enemy(self):
        for enemy in self.game_data['Enemy']:
            if enemy['x'] == self.player_data['Player_Start']['x']+1 and enemy['y'] == self.player_data['Player_Start']['y']:
                self.game_data['Enemy'].remove(enemy)
                self.update_score(10)# Award points for defeating an enemy
                self.enemy_count -= 1
                break  # Only attack one enemy at a time
            elif enemy['x'] == self.player_data['Player_Start']['x']-1 and enemy['y'] == self.player_data['Player_Start']['y']:
                self.game_data['Enemy'].remove(enemy)
                self.update_score(10)
                self.enemy_count -= 1
                break
            elif enemy['x'] == self.player_data['Player_Start']['x'] and enemy['y'] == self.player_data['Player_Start']['y']+1:
                self.game_data['Enemy'].remove(enemy)
                self.update_score(10)
                self.enemy_count -= 1
                break
            elif enemy['x'] == self.player_data['Player_Start']['x'] and enemy['y'] == self.player_data['Player_Start']['y']-1:
                self.game_data['Enemy'].remove(enemy)
                self.update_score(10)
                self.enemy_count -= 1
                break

    def check_obstacle_collision(self, x, y):
        # Check if the position (x, y) is an obstacle
        if x < 0 or x >= self.game_data["Board_Width"] or y < 0 or y >= self.game_data["Board_Height"]:
            return True  # Collision with wall
        for obstacle in self.game_data['Obstacle']:
            if obstacle['x'] == x and obstacle['y'] == y:
                return True  # Collision detected
        return False  # No collision

    def check_enemy_collision(self,x,y):
        # Check if the player has collided with an enemy and update health/score accordingly
        for enemy in self.game_data['Enemy']:
            if enemy['x'] == x and enemy['y'] == y:
                self.player_data["Player_Health"] -= 1
                return True  # Collision occurred
        return False  # No collision
    
    def check_enemy_on_enemy(self, x, y):
        # Check if the position (x, y) is occupied by an enemy
        for enemy in self.game_data['Enemy']:
            if enemy['x'] == x and enemy['y'] == y:
                return True  # Collision with another enemy
        return False  # No collision with another enemy

    def update_score(self, points):
        self.player_data["Player_Score"] += points

    def check_game_over(self):
        if self.player_data["Player_Health"] <= 0:
            return True
        return False

    def spawn_collectible(self):
        pass

    def spawn_enemy(self):
        if self.enemy_count >= 7:
            return
        # added a random chance to spawn an enemy each turn, and a limit on the total number of enemies that can be present at once.
        if random.random() > 0.3:
            return        
        # Spawn an enemy at a random position that is not an obstacle
        x = random.randint(0, self.game_data["Board_Width"] - 1)
        y = random.randint(0, self.game_data["Board_Height"] - 1)
        if not self.check_obstacle_collision(x, y):
            random_enemy_icon = random.choice([self.game_data['skeleton'], self.game_data['zombie']])
            self.game_data['Enemy'].append({'x': x, 'y': y, 'icon': random_enemy_icon})
            self.enemy_count += 1

    def move_enemies(self):
        # Move each enemy randomly in one of the four directions, ensuring they stay within bounds and downt run into obstacles. This function can be called after the player moves to create a more dynamic game environment.
        for enemy in self.game_data['Enemy']:
            direction = random.choice(['up', 'down', 'left', 'right'])
            new_x = enemy['x']
            new_y = enemy['y']
            if direction == 'up':  # Up
                new_y -= 1
            elif direction == 'down':  # Down
                new_y += 1
            elif direction == 'left':  # Left
                new_x -= 1
            elif direction == 'right':  # Right
                new_x += 1

            # Check for boundaries and obstacles
            if not self.check_obstacle_collision(new_x, new_y) and not self.check_enemy_on_enemy(new_x, new_y):
                enemy['x'] = new_x
                enemy['y'] = new_y
        
    def play_game(self,stdscr):
        # Main game loop to handle player input, update game state, and redraw the board
        
        stdscr.nodelay(False)

        while not self.check_game_over():
            # Get player input and move player accordingly
            try:
                key  = stdscr.getkey()
            except curses.error:
                key = None
            
            if key is None:
                continue

            if key.lower() == 'q':
                break
            
            self.move_player(key.lower())
            self.move_enemies()
            self.spawn_enemy()
            self.spawn_collectible()
            self.draw_board(stdscr)

        print("Game Over!\nFinal Score:", self.player_data["Player_Score"])    


adventure_game = Game()
# Use curses.wrapper with a callable that accepts the stdscr argument.
curses.wrapper(adventure_game.play_game)
