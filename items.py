import numpy as np

class Storage:

    def __init__(self, sprite_key_border, sprite_key_internal, window_size, size, initial_items = None):
        self.items = initial_items
        self.sprite_key_border = sprite_key_border
        self.sprite_key_internal = sprite_key_internal
        self.size = size
        self.window_size = window_size

    # def display(self, bool, position):
    #     if bool:
    #         for i in range(0, self.size[0]):
    #             for j in range(0, self.size[1]):



# class Item:
#     def __init__(self, name, sprite_key):
#         self.name = name
#         self.sprite_key = sprite_key
#
#     def display_in_invetory(self, position):
#         disp()
#
#     def disp_in_hand(self):



class Weapon:
    def __init__(self, name, sprite_key, attack_range, base_damage, damage_multiplier=None):
        # super(name, sprite_key)
        self.name = name
        self.range = attack_range                           # Int: 1 to 10. If 1, it's a melee weapon.
        self.base_damage = base_damage                      # 2D Int vector [number_of_die, dice_value]
        self.damage_multiplier = damage_multiplier          # Dictionary; {'Attribute': [], 'Multiplier': []}

    def get_damage(self, character):
        damage = 0
        max_dice_value = self.base_damage[1]
        for dice in range(0, self.base_damage[0]):
            roll = max_dice_value
            while roll == max_dice_value:
                roll = np.random.randint(1, high=max_dice_value+1)
                damage += roll
        return damage
        # for [attribute, multiplier] in zip(self.damage_multiplier['Attribute'], self.damage_multiplier['Multiplier']):

    def upgrade(self, new_base_damage):
        self.base_damage = new_base_damage

    def change_sprite(self, new_sprite_key):
        self.sprite_key = new_sprite_key

sword = Weapon('Sword',0, 1, [2, 4])
bow = Weapon('Bow',0, 4, [1, 8])

