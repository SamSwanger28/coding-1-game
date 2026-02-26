    # Write your game here
import curses
import random

class Game():
    def __init__(self):
        self.game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons
    'Board_Width' : 25,
    'Board_Height' : 20,
    'Obstacle_data' : [], # Will be populated with random obstacles

    # Board pngs
    'obstacle': "\U0001FAA8 ",# 🪨
    'cactus': "\U0001F335 ", # 🌵
    'empty': "  ",
    'skeleton' : "\U0001F480", # 💀
    'zombie': "\U0001F9DF", # 🧟  
    'ruppee' : "\U0001F48E", # 💎
    }

    def draw_board(self, stdscr, enemy_manager, collectible_manager, player, shop_manager):
        # Print the board and all game elements using curses
        stdscr.clear()
        for y in range(self.game_data["Board_Height"]):
            row = " "
            # build the entire row first, then draw it once
            for x in range(self.game_data['Board_Width']):
                if player.player_data["Player_Start"]["x"] == x and player.player_data["Player_Start"]["y"] == y:
                    row += player.player_data['Player_Icon']
                elif any(o["x"] == x and o["y"] == y for o in self.game_data['Obstacle_data']):
                    obstacle = next(o for o in self.game_data['Obstacle_data'] if o["x"] == x and o["y"] == y)
                    row += obstacle['icon']
                elif any(e["x"] == x and e["y"] == y for e in enemy_manager.enemy_locations):
                    enemy = next(e for e in enemy_manager.enemy_locations if e["x"] == x and e["y"] == y)
                    row += enemy['icon']
                elif any(c["x"] == x and c["y"] == y for c in collectible_manager.collectibles):
                    collectible = next(c for c in collectible_manager.collectibles if c["x"] == x and c["y"] == y)
                    row += collectible['icon']
                elif shop_manager.shop_data['x'] == x and shop_manager.shop_data['y'] == y:
                    row += shop_manager.shop_data['icon']
                else:
                    row += self.game_data['empty']
            try:
                stdscr.addstr(y, 0, row, curses.color_pair(1))
            except curses.error:
                pass
        try:
            stdscr.addstr(self.game_data["Board_Height"] + 1, 20, f"Score: {player.player_data['Player_Score']} ")
            stdscr.addstr(self.game_data["Board_Height"] + 2, 1, "Move with W/A/S/D, Press G to attack, H to heal, B to shop when by the shop, Q to quit")
            stdscr.addstr(self.game_data["Board_Height"] + 1, 1, f"Health: {player.player_data['Player_Health']} ")
            stdscr.addstr(self.game_data["Board_Height"] + 1, 35, f"Health Potions: {player.player_data['Health_Potion'],}")
        
        except curses.error:
            # My code is being weird and sometimes throws an error when trying to print the score/health. This is a workaround to prevent it from crashing.
            pass
        stdscr.refresh()

    def randomize_obstacles(self, player, enemy_manager):
        # Randomly place obstacles on the board, ensuring they don't overlap with the player, enemies, or other obstacles
        self.game_data['Obstacle_data'].clear()
        while len(self.game_data['Obstacle_data']) < 25:
            x = random.randint(0, self.game_data["Board_Width"] - 1)
            y = random.randint(0, self.game_data["Board_Height"] - 1)
            # skip if player, any enemy, or an existing obstacle occupies this spot
            if (x, y) == (player.player_data["Player_Start"]["x"], player.player_data["Player_Start"]["y"]):
                continue
            if any(e["x"] == x and e["y"] == y for e in enemy_manager.enemy_locations):
                continue
            if any(o["x"] == x and o["y"] == y for o in self.game_data['Obstacle_data']):
                continue
            obstacle_icon = random.choice([self.game_data['obstacle'], self.game_data['cactus']])
            self.game_data['Obstacle_data'].append({'x': x, 'y': y, 'icon': obstacle_icon}) # 🌵

class Player(): 
    def __init__(self):
        self.player_data = {       
            'Player_Start' : {'x' : 2,'y' : 10},
            'Weapon_Start' : {'x' : 3, 'y' : 10},
            'Player_Health' : 5,
            'Player_Score' : 0,
            'Player_Icon' : "\U0001F9DD", # 🧝
            'Player_Weapon' : 'sword',
            'Health_Potion' : 3,
            'Diangonals_Unlocked' : True,
            'Damage_Reduction_Unlocked' : False
            }
    
    def attack_enemy(self, enemy_manager,x,y):
        for enemy in enemy_manager.enemy_locations:
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if enemy['x'] == i and enemy['y'] == j:
                        enemy_manager.enemy_locations.remove(enemy)
                        enemy_manager.enemy_count -= 1
                        self.update_score(10)  # Award points for defeating an enemy
                        return True  # Enemy attacked
    
    def update_score(self, points):
        self.player_data["Player_Score"] += points

    def move_player(self, direction, enemy_manager, collectible_manager,game_type):
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
            self.attack_enemy(enemy_manager,new_x,new_y)
            return
        elif direction == 'h':  # Use health potion
            if self.player_data['Health_Potion'] > 0 and self.player_data['Player_Health'] < 5:
                self.player_data['Player_Health'] += 1
                self.player_data['Health_Potion'] -= 1
            return
        elif direction == 'b':  # Interact with shop
            if game_type.game_data['Shop_data']['x'] == self.player_data['Player_Start']['x'] and game_type.game_data['Shop_data']['y'] == self.player_data['Player_Start']['y']:
                shop_manager.interact_with_shop(self, curses.initscr())
            return
        # Check for boundaries
        if not check_obstacle_collision(new_x, new_y, game_type, interacter=self):
            self.player_data["Player_Start"]["x"] = new_x
            self.player_data["Player_Start"]["y"] = new_y
            self.check_enemy_collision(enemy_manager)
            self.check_collectible_collision(collectible_manager)

    def check_enemy_collision(self, enemy_manager):
    # Check if the player has collided with an enemy and update health/score accordingly
        for enemy in enemy_manager.enemy_locations:
            if enemy['x'] == self.player_data['Player_Start']['x'] and enemy['y'] == self.player_data['Player_Start']['y']:
                self.player_data["Player_Health"] -= 1
                return True  # Collision occurred
        return False  # No collision

    def check_collectible_collision(self,collectible_manager):
        # Check if the player has collided with a collectible and update score accordingly
        for collectible in collectible_manager.collectibles:
            if collectible['x'] == self.player_data['Player_Start']['x'] and collectible['y'] == self.player_data['Player_Start']['y']:
                self.update_score(20)  # Award points for collecting an item
                collectible_manager.collectibles.remove(collectible)
                collectible_manager.collectible_count -= 1
                return True  # Collision occurred
        return False  # No collision

    def check_game_over(self):
        if self.player_data["Player_Health"] <= 0:
            return True
        return False

class Enemy():
    def __init__(self):
        self.enemy_count = 2
        self.enemy_data = {
            "enemy_types": ["skeleton", "zombie"],
            "enemy_locations": [
                {'x': 5, 'y': 5, 'icon': "\U0001F9DF"}, # 🧟
                {'x': 15, 'y': 15, 'icon': "\U0001F480"}] # 💀
        }
        self.enemy_locations = self.enemy_data["enemy_locations"]
    
    def move_enemies(self, player, game_type):
        # Move each enemy randomly in one of the four directions, ensuring they stay within bounds and downt run into obstacles. This function can be called after the player moves to create a more dynamic game environment.
        for enemy in self.enemy_locations[:]:  # Iterate over a copy to safely remove items
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

            # Check if enemy moves into player position
            if new_x == player.player_data['Player_Start']['x'] and new_y == player.player_data['Player_Start']['y']:
                player.player_data['Player_Health'] -= 1
                self.enemy_locations.remove(enemy)
                self.enemy_count -= 1
            # Check for boundaries and obstacles
            elif not check_obstacle_collision(new_x, new_y, game_type, interacter=self) and not self.check_enemy_on_enemy(new_x, new_y):
                enemy['x'] = new_x
                enemy['y'] = new_y
    
    def spawn_enemy(self, game_type):
        if self.enemy_count >= 7:
            return
        # added a random chance to spawn an enemy each turn, and a limit on the total number of enemies that can be present at once.
        if random.random() > 0.3:
            return        
        # Spawn an enemy at a random position that is not an obstacle
        x = random.randint(0, game_type.game_data["Board_Width"] - 1)
        y = random.randint(0, game_type.game_data["Board_Height"] - 1)
        if not check_obstacle_collision(x, y, game_type) and not self.check_enemy_on_enemy(x, y):
            random_enemy_icon = random.choice([game_type.game_data['skeleton'], game_type.game_data['zombie']])
            self.enemy_locations.append({'x': x, 'y': y, 'icon': random_enemy_icon})
            self.enemy_count += 1
    
    def check_enemy_on_enemy(self, x, y):
        # Check if the position (x, y) is occupied by an enemy
        for enemy in self.enemy_locations:
            if enemy['x'] == x and enemy['y'] == y:
                return True  # Collision with another enemy
        return False  # No collision with another enemy

class Collectible():
    def __init__(self):
        self.collectibles = []
        self.collectible_count = 0  

    def spawn_collectible(self, game_type,enemy_manager):
        if self.collectible_count >= 5:
            return
        # Spawn a collectible at a random position that is not an obstacle or enemy
        x = random.randint(0, game_type.game_data["Board_Width"] - 1)
        y = random.randint(0, game_type.game_data["Board_Height"] - 1)
        if not check_obstacle_collision(x, y, game_type) and not enemy_manager.check_enemy_on_enemy(x, y):
            self.collectibles.append({'x': x, 'y': y, 'icon': game_type.game_data['ruppee']})
            self.collectible_count += 1

def play_game(stdscr,game_type,player,enemy_manager,collectible_manager,shop_manager):
        # Main game loop to handle player input, update game state, and redraw the board
        game_type.randomize_obstacles(player, enemy_manager)

        collectible_manager.spawn_collectible(game_type,enemy_manager)

        # welcome_player(stdscr) 
        
        game_type.draw_board(stdscr, enemy_manager, collectible_manager,player,shop_manager)

        stdscr.nodelay(False)

        while not player.check_game_over():
            # Get player input and move player accordingly
            try:
                key  = stdscr.getkey()
            except curses.error:
                key = None

            if key.lower() == 'q':
                break
            
            player.move_player(key.lower(), enemy_manager, collectible_manager, game_type)
            enemy_manager.move_enemies(player,game_type)
            enemy_manager.spawn_enemy(game_type)
            collectible_manager.spawn_collectible(game_type,enemy_manager)
            game_type.draw_board(stdscr, enemy_manager, collectible_manager,player,shop_manager)
        while True:
            stdscr.clear()
            stdscr.addstr(10, 10, f"Game Over! Final Score: {player.player_data['Player_Score']}")
            stdscr.addstr(11, 10, "Press N to start a new game or Q to quit.")
            stdscr.refresh()
            try:
                key = stdscr.getkey()
            except curses.error:
                key = None
            if key.lower() == 'n':
                # reinitialize game objects so state is clean
                player.__init__()
                game_type.__init__()
                enemy_manager.__init__()
                collectible_manager.__init__()
                play_game(stdscr, game_type, player, enemy_manager, collectible_manager)
                break
            elif key.lower() == 'q':
                break

def welcome_player(stdscr):
        stdscr.clear()
        stdscr.addstr(10, 10, "Welcome to the Adventure Game!")
        stdscr.addstr(11, 10, "Move with W/A/S/D, Press G to attack,H to heal, B to shop when by the shop, Q to quit")
        stdscr.addstr(12, 10, "Defeat enemies and survive as long as you can!")
        stdscr.refresh()
        stdscr.getch()  # Wait for player to press a key

def check_obstacle_collision(x, y, game, interacter=None):
    # Check if the position (x, y) is out of bounds or occupied by an obstacle
    if x < 0 or x >= game.game_data["Board_Width"] or y < 0 or y >= game.game_data["Board_Height"]:
        return True
    for obstacle in game.game_data['Obstacle_data']:
        if obstacle['x'] == x and obstacle['y'] == y:
            if obstacle['icon'] == game.game_data['cactus'] and interacter is not None:  # If it's a cactus and we have an interacter (player or enemy)
                if isinstance(interacter, Player):
                    interacter.player_data['Player_Health'] -= 1  # Cacti deal damage on collision
                elif isinstance(interacter, Enemy):
                    pass
            return True
    return False

class Shop():
    def __init__(self):
        self.items = {
            'Damage Reduction': {'cost': 175, 'description': 'Take less damage from enemies', 'icon': "\U0001F6E1"}, # 🛡
            'Health Potion': {'cost': 300, 'description': 'Restore 1 health points', 'icon': "\U0001F9C0"}, # 🧃
            'Aoe Attack': {'cost': 350, 'description': 'Attack all adjacent enemies', 'icon': "\U0001F32A"}, # 🌪
        }
        
        self.shop_data = {
            'icon': "\U0001F3EA", # 🏪
            'x' : 24,
            'y' : 19
        }
    def interact_with_shop(self, player, stdscr):
        stdscr.clear()
        stdscr.addstr(1,1, "Welcome to my shop! You may browse my wares and obtain items to aid you in your deadly travles.")
        stdscr.addstr(2,1, f"You have {player.player_data['Player_Score']} rupees.")
        stdscr.addstr(4,1, "Items for sale:")
        for i, (item_name, item_info) in enumerate(self.items.items(), start=1):
            stdscr.addstr(5+i, 3, f"{i}. {item_info['icon']} {item_name} - {item_info['cost']} rupees")
            stdscr.addstr(5+i, 40, f"{item_info['description']}")
        stdscr.addstr(11,1, "Press the number of the item you wish to purchase, or B to exit the shop.")
        stdscr.refresh()
        while True:            
            try:
                key = stdscr.getkey()
            except curses.error:
                key = None
            if key.lower() == 'b':
                break   
            elif key in ['1', '2', '3']:
                item_index = int(key) - 1
                if item_index < len(self.items):
                    item_name = list(self.items.keys())[item_index]
                    item_info = self.items[item_name]
                    if player.player_data['Player_Score'] >= item_info['cost']:
                        player.player_data['Player_Score'] -= item_info['cost']
                        if item_name == 'Damage Reduction':
                            player.player_data['Damage_Reduction_Unlocked'] = True
                        elif item_name == 'Health Potion':
                            player.player_data['Health_Potion'] += 1
                        elif item_name == 'Aoe Attack':
                            pass  # Implement AOE attack functionality as needed
                        stdscr.addstr(17,1, f"You purchased {item_name}!")
                    else:
                        stdscr.addstr(17,1, "You don't have enough rupees for that item.")
                    stdscr.refresh()

shop_manager = Shop()
player_one = Player()
adventure_game = Game()
enemy_manager = Enemy()
collectible_manager = Collectible()
curses.wrapper(play_game, adventure_game, player_one, enemy_manager, collectible_manager, shop_manager)
# shop_manager.interact_with_shop(player_one, curses.initscr())