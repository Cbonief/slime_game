import pygame
import os
from items import *
from level_generator import create_level
from path_finding import *
from character import *

moveEvents = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
params_translate = [
    {'Up': 0, 'Down': 0, 'Left': -1, 'Right': 0},
    {'Up': -1, 'Down': 0, 'Left': 0, 'Right': 0}
]

dir_names = ['Up', 'Down', 'Left', 'Right']


class Game:
    def __init__(self, window):
        self.width = window.get_width()
        self.height = window.get_height()
        self.window = window

        self.timer = {
            'Player_Movement': {'Value': 0, 'Period': 100, 'Function': self.player_movement_handler},
            'Enemies_Movement': {'Value': 0, 'Period': 500, 'Function': self.enemies_movement_handler},
            'Attack': {'Value': 0, 'Period': 100, 'Function': self.combat_handler},
            'Projectiles': {'Value': 0, 'Period': 10, 'Function': self.projectiles_handler}
        }
        self.index = 0
        self.screen_size = [15, 13]
        self.off_set = [int((self.screen_size[0]-1)/2), int((self.screen_size[1]-1)/2)]
        print(self.off_set)
        self.size_x = round(self.width / self.screen_size[0])
        self.size_y = round(self.height / self.screen_size[1])
        self.floor = pygame.image.load(os.path.join("Game Images/tiles", "generic-rpg-Slice.png"))
        self.floor = pygame.transform.scale(self.floor, (self.size_x, self.size_y))

        tiles = pygame.image.load(os.path.join("Game Images/jawbreaker", "sample.png"))
        self.tiles = []
        for i in range(0, int(tiles.get_width()/16)):
            for j in range(0, int(tiles.get_height()/16)):
                new_tile = pygame.Surface((16, 16))
                new_tile.blit(tiles, (0, 0), (i*16, j*16, 16, 16))
                new_tile = pygame.transform.scale(new_tile, (self.size_x, self.size_y))
                self.tiles.append(new_tile)

        self.empty = pygame.image.load(os.path.join("Game Images", "empty.png"))
        self.empty = pygame.transform.scale(self.empty, (self.size_x, self.size_y))
        self.char = pygame.image.load(os.path.join("Game Images", "character-removebg-preview.png")).convert_alpha()
        self.char = aspect_scale_x(self.char, self.size_x)
        self.char_images = {
            'Up': self.char,
            'Down': pygame.transform.flip(self.char, False, True),
            'Left': pygame.transform.rotate(self.char, 90),
            'Right': pygame.transform.rotate(self.char, -90)
        }
        self.grass_door = pygame.image.load(os.path.join("Game Images", "door.png"))
        self.door = {
            'Up': pygame.transform.scale(self.grass_door, (self.size_x, self.size_y)),
            'Down': pygame.transform.flip(pygame.transform.scale(self.grass_door, (self.size_x, self.size_y)), False, True),
            'Left': pygame.transform.scale(pygame.transform.rotate(self.grass_door, 90), (self.size_x, self.size_y)),
            'Right': pygame.transform.scale(pygame.transform.rotate(self.grass_door, -90), (self.size_x, self.size_y))
        }
        self.floors = []
        floor = pygame.image.load(os.path.join("Game Images", "floor_with_non.png"))
        floor = pygame.transform.scale(floor, (self.size_x, self.size_y))
        self.floors.append(floor)
        floor = pygame.image.load(os.path.join("Game Images", "floor_with_grass.png"))
        floor = pygame.transform.scale(floor, (self.size_x, self.size_y))
        self.floors.append(floor)
        floor = pygame.image.load(os.path.join("Game Images", "floor_with_grass2.png"))
        floor = pygame.transform.scale(floor, (self.size_x, self.size_y))
        self.floors.append(floor)
        floor = pygame.image.load(os.path.join("Game Images", "floor_with_grass3.png"))
        floor = pygame.transform.scale(floor, (self.size_x, self.size_y))
        self.floors.append(floor)
        floor = pygame.image.load(os.path.join("Game Images", "floor_with_rock.png"))
        floor = pygame.transform.scale(floor, (self.size_x, self.size_y))
        self.floors.append(floor)

        self.wall = pygame.image.load(os.path.join("Game Images", "wall.png"))
        self.wall = pygame.transform.scale(self.wall, (self.size_x, self.size_y))

        self.arrow = pygame.image.load(os.path.join("Game Images", "arrow.png")).convert_alpha()
        self.arrow = pygame.transform.scale(self.arrow, (int(self.size_x/2), int(self.size_y/2)))

        self.play = True
        self.gridSize = [100, 100]
        [self.grid, self.door_direction, self.feasible_positions] = create_level(self.gridSize, self.off_set, startingWalkers=5, chanceWalkerChangeDir=0.2, chanceWalkerSpawn=0.05, chanceWalkerDestroy=0.05, maxWalkers=0, percentToFill=0.2)
        self.grid_tile = {

        }
        for key in self.feasible_positions:
            self.grid_tile[key] = np.random.choice(self.floors, p=[0.5, 0.15, 0.15, 0.15, 0.05])

        # Characters
        player = Character(get_random_from_dictionary(self.feasible_positions), 100, name='Bob')       # Player
        player.equip(sword)
        enemy1 = Character(get_random_from_dictionary(self.feasible_positions), 100, name='Spider')    # NPC 1
        enemy2 = Character(get_random_from_dictionary(self.feasible_positions), 100, name='Nelson')    # NPC 2
        # Dictionary containing all characters.
        self.characters = {
            'Player': player,
            'Enemy 1': enemy1,
            'Enemy 2': enemy2
        }

        self.projectiles = {
            'Player': {'Target': None, 'Position': [0, 0], 'Rotation': 0, 'Tick': 0, 'Disp': False},
            'Enemy 1': None,
            'Enemy 2': None
        }

        self.enemies_move = [None, None]
        self.move = None
        self.player_moved = False
        self.dash = False

    def display_all(self):
        self.display_grid()
        self.display_character()
        self.display_projectiles()

    def display_grid(self):
        for [i, translate_x] in zip(range(0, self.screen_size[0]), range(self.characters['Player'].pos[0] - self.off_set[0], self.characters['Player'].pos[0] + self.off_set[0] + 1)):
            for [j, translate_y] in zip(range(0, self.screen_size[1]), range(self.characters['Player'].pos[1] - self.off_set[1], self.characters['Player'].pos[1] + self.off_set[1] + 1)):
                floor = self.grid[translate_x][translate_y]
                draw_pos = (i * self.size_x, j * self.size_y)
                if floor == 'w':
                    self.window.blit(self.wall, draw_pos)
                elif floor == 'e':
                    self.window.blit(self.empty, draw_pos)
                elif floor == 'f':
                    self.window.blit(self.grid_tile[hash_from_list([translate_x, translate_y], self.gridSize)], draw_pos)
                elif floor == 'd':
                    self.window.blit(self.door[self.door_direction], draw_pos)

    def display_character(self):
        dif = self.char.get_height() - self.size_x
        for [name, character] in self.characters.items():
            distance_x = character.pos[0] - self.characters['Player'].pos[0]
            distance_y = character.pos[1] - self.characters['Player'].pos[1]
            if -self.off_set[0] <= distance_x <= self.off_set[0] and -self.off_set[1] <= distance_y <= self.off_set[1]:
                pos_x = int((self.off_set[0] + distance_x) * self.size_x)
                pos_y = int((self.off_set[1] + distance_y) * self.size_y)

                if name == self.characters['Player'].current_enemy:
                    pygame.draw.rect(self.window, (255, 0, 0), (pos_x, pos_y, self.size_x, self.size_y), 1)

                health = character.current_health
                health_bar = int(50 * health / character.max_health)

                pygame.draw.rect(self.window, (0, 0, 0), (pos_x, pos_y, 50, 5))
                if health >= 50:
                    pygame.draw.rect(self.window, (0, 255, 0), (pos_x, pos_y, health_bar, 5))
                elif 25 <= health < 50:
                    pygame.draw.rect(self.window, (255, 165, 0), (pos_x, pos_y, health_bar, 5))
                elif 0 < health < 25:
                    pygame.draw.rect(self.window, (255, 50, 0), (pos_x, pos_y, health_bar, 5))

                pos_x = int(pos_x + params_translate[0][character.dir] * dif)
                pos_y = int(pos_y + params_translate[1][character.dir] * dif)

                self.window.blit(self.char_images[character.dir], [pos_x, pos_y])

    def display_projectiles(self):
        if self.projectiles['Player']['Disp']:
            change_x = self.projectiles['Player']['Position'][0] - self.characters['Player'].pos[0]
            change_y = self.projectiles['Player']['Position'][1] - self.characters['Player'].pos[1]
            if -5 <= change_x < 6 and -5 <= change_y < 6:
                pos_x = int((5 + change_x) * self.size_x)
                pos_y = int((5 + change_y) * self.size_y)
                self.window.blit(pygame.transform.rotate(self.arrow, self.projectiles['Player']['Rotation']), [pos_x, pos_y])

    def get_grid_coordinates(self, coordinates):
        found_row = False
        found_col = False
        i = 0
        translate_x = self.characters['Player'].pos[0] - self.off_set[0]
        j = 0
        translate_y = self.characters['Player'].pos[1] - self.off_set[1]
        grid_coordinates = [0, 0]

        while not found_row and i < self.screen_size[0] and translate_x <= self.characters['Player'].pos[0] + self.off_set[0]:
            boundary = (i + 1) * self.size_x
            if boundary >= coordinates[0]:
                found_row = True
                grid_coordinates[0] = translate_x
            i += 1
            translate_x += 1

        while not found_col and j < self.screen_size[1] and translate_y <= self.characters['Player'].pos[1] + self.off_set[1]:
            boundary = (j + 1) * self.size_y
            if boundary >= coordinates[1]:
                found_col = True
                grid_coordinates[1] = translate_y
            j += 1
            translate_y += 1

        return grid_coordinates

    def run(self):
        clock = pygame.time.Clock()                 # Cria o clock do jogo.

        # Inicia o loop do jogo.
        while self.play:
            dt = clock.tick(60)                     # Seta o FPS, e retorna o tempo desde o último frame.

            # Cuida dos timers.
            for timer_name in self.timer:
                self.timer[timer_name]['Value'] += dt
                if self.timer[timer_name]['Value'] >= self.timer[timer_name]['Period']:
                    self.timer[timer_name]['Value'] -= self.timer[timer_name]['Period']
                    self.timer[timer_name]['Function']()

            # Coloca todas as texturas na tela.
            self.display_all()

            # Cuida de todos os eventos do usuário que aconteceram.
            self.event_loop()

            if self.player_moved:
                index = 0
                for [name, character] in self.characters.items():
                    if name is not 'Player' and get_distance(character.pos, self.characters['Player'].pos) < 8:
                        moves = find_path_moves(character.pos, self.characters['Player'].pos, self.grid, self.gridSize)
                        self.enemies_move[index] = moves.head
                        index += 1

            if self.characters['Player'].is_attacking and self.characters['Player'].equipped_weapon.range == 1:
                moves = find_path_moves(self.characters['Player'].pos, self.characters[self.characters['Player'].current_enemy].pos, self.grid, self.gridSize)
                self.move = moves.head

            pygame.display.update()

    def combat_handler(self):
        if self.characters['Player'].is_attacking:
            attack_range = self.characters['Player'].equipped_weapon.range
            if get_distance(self.characters['Player'].pos, self.characters[self.characters['Player'].current_enemy].pos) <= attack_range:
                if attack_range == 1:
                    damage = self.characters['Player'].equipped_weapon.get_damage()
                    self.characters[self.characters['Player'].current_enemy].current_health -= damage
                    if self.characters[self.characters['Player'].current_enemy].current_health < 0:         # Se morreu
                        del self.characters[self.characters['Player'].current_enemy]
                        self.characters['Player'].is_attacking = False
                else:
                    if self.projectiles['Player']['Target'] is None:
                        self.projectiles['Player']['Target'] = self.characters['Player'].current_enemy
                        start = self.characters['Player'].pos
                        self.projectiles['Player']['Position'] = np.array(start)
                        self.projectiles['Player']['Tick'] = 1
                        self.projectiles['Player']['Disp'] = True
                    elif is_inside_square(self.projectiles['Player']['Position'], self.characters[self.projectiles['Player']['Target']].pos):
                        damage = self.characters['Player'].equipped_weapon.get_damage()
                        self.characters[self.characters['Player'].current_enemy].current_health -= damage
                        if self.characters[self.characters['Player'].current_enemy].current_health < 0:
                            del self.characters[self.characters['Player'].current_enemy]
                            self.characters['Player'].is_attacking = False
                        self.projectiles['Player']['Target'] = None
                        self.projectiles['Player']['Disp'] = False
                        self.projectiles['Player']['Tick'] = 1
                        self.projectiles['Player']['Position'] = np.array([0, 0])

    def player_movement_handler(self):
        if self.move is not None:
            self.characters['Player'].move(self.move, self.grid, list(self.characters.values()))
            self.move = self.move.next
            self.player_moved = True
        else:
            self.player_moved = False
            self.dash = False
            self.timer['Player_Movement']['Period'] = 100

    def enemies_movement_handler(self):
        index = 0
        for [name, character] in self.characters.items():
            if name is not 'Player':
                if get_distance(character.pos, self.characters['Player'].pos) < 8:
                    if self.enemies_move[index] is not None:
                        character.move(self.enemies_move[index], self.grid, list(self.characters.values()))
                        self.enemies_move[index] = self.enemies_move[index].next
                else:
                    self.enemies_move[index] = None
                index += 1

    def projectiles_handler(self):
        # Move projectile
        if self.projectiles['Player']['Target'] is not None:
            goal = self.characters[self.projectiles['Player']['Target']].pos
            start = self.projectiles['Player']['Position']
            print('Start: ', start)
            print('Goal: ', goal)
            change = np.subtract(goal, start)
            print('Change: ', change)
            change = np.multiply(change, self.projectiles['Player']['Tick']/10)
            self.projectiles['Player']['Position'] = np.add(self.projectiles['Player']['Position'], change)
            self.projectiles['Player']['Rotation'] = 0
            self.projectiles['Player']['Tick'] += 1

    def event_loop(self):
        # Passa por todos os eventos detectados no frame.
        for event in pygame.event.get():

            # Quit the game
            if event.type == pygame.QUIT:
                self.play = False

            # Mouse checks.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_grid_coordinates = self.get_grid_coordinates(pygame.mouse.get_pos())
                mouse_grid_coordinates_hash = hash_from_list(mouse_grid_coordinates, self.gridSize)

                # Check if the player has clicked on a NPC.
                if not compare(self.characters['Player'].pos, mouse_grid_coordinates_hash, self.gridSize):
                    player_attack = False
                    for [enemy_name, enemy] in self.characters.items():
                        if compare(enemy.pos, mouse_grid_coordinates_hash, self.gridSize):
                            self.characters['Player'].attack(enemy_name)
                            player_attack = True

                    # Check if the player can move to the clicked location. If so, he moves.
                    if get_grid_tile(self.grid, mouse_grid_coordinates) == 'f' and not player_attack:
                        moves = find_path_moves(self.characters['Player'].pos, mouse_grid_coordinates, self.grid, self.gridSize)
                        self.move = moves.head

            # Keyboard checks.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.dash:
                    self.move = Move(self.characters['Player'].dir)
                    self.move.next = Move(self.characters['Player'].dir)
                    self.move.next.next = Move(self.characters['Player'].dir)
                    self.timer['Player_Movement']['Period'] = 30
                    self.dash = True

                for index in range(0, 4):
                    if event.key == moveEvents[index]:
                        self.move = Move(dir_names[index])


def aspect_scale_x(img, bx):
    ix, iy = img.get_size()
    scale_factor = bx/float(ix)
    sx = round(scale_factor * ix)
    sy = round(scale_factor * iy)

    return pygame.transform.scale(img, (sx, sy))


def get_random_from_dictionary(dictionary):
    return dictionary[np.random.choice(list(dictionary.keys()))]


def get_grid_tile(grid, coordinates):
    return grid[coordinates[0]][coordinates[1]]


def is_inside_square(position, square_coordinate):
    for margim in [-0.1, 0.1]:
        inside = True
        for index in [0, 1]:
            if not (square_coordinate[index] <= position[index] + margim < square_coordinate[index] + 1):
                inside = False
        if inside:
            return True
    return False

