import numpy as np
from items import *


class Character:
    def __init__(self, pos=None, health=100, level=1, name=None):
        # Base attributes variables
        self.name = name
        self.max_health = health
        self.current_health = health
        self.attributes = {
            'Strength': 1,
            'Agility': 1,
            'Wisdom': 1,
            'Willpower': 1,
            'Vitality': 1
        }
        self.skills = None
        self.level = level

        # Inventory and items variables
        self.equipped_weapon = None
        self.equipped_armor = None
        self.inventory = None

        # Combat variables
        self.is_attacking = False
        self.current_enemy = None

        # Positional and movement variables
        self.pos = np.array(pos)
        self.dir = 'Up'


    def move(self, move, map_grid, characters):
        direction = move.direction
        self.dir = move.direction
        new_pos = np.add(self.pos, move_directions[direction])
        feasible = True
        index = 0
        while feasible and index < len(characters):
            character = characters[index]
            if character.pos[0] == new_pos[0] and character.pos[1] == new_pos[1]:
                feasible = False
            index += 1
        if map_grid[new_pos[0]][new_pos[1]] == 'f' and feasible:
            self.pos = new_pos

    def attack(self, enemy_name):
        if enemy_name == self.current_enemy:
            self.is_attacking = False
            self.current_enemy = None
        else:
            self.current_enemy = enemy_name
            self.is_attacking = True

    def equip(self, weapon):
        self.equipped_weapon = weapon


move_directions = {
    'Up':       [0, -1],
    'Down':     [0, 1],
    'Left':     [-1, 0],
    'Right':    [1, 0]
}

dir_names = ['Up', 'Down', 'Left', 'Right']


class Move:
    def __init__(self, direction=None, start=None, finish=None):
        if direction is None and start is not None and finish is not None:
            if finish[1] - start[1] == 1:
                self.direction = 'Down'
            elif finish[1] - start[1] == -1:
                self.direction = 'Up'
            elif finish[0] - start[0] == 1:
                self.direction = 'Right'
            elif finish[0] - start[0] == -1:
                self.direction = 'Left'
        else:
            self.direction = direction
        self.next = None


class Moves:
    def __init__(self, initial_move=None):
        self.head = initial_move
        self.last = self.head

    def add_move_end(self, move):
        if self.head is None:
            self.head = move
        else:
            if self.last is None:
                last = self.head
            else:
                last = self.last
            last.next = move
        self.last = move

    def add_move_begin(self, move):
        if self.head is None:
            self.head = move
            self.last = move
        else:
            move.next = self.head
            self.head = move
