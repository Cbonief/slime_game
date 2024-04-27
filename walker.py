import numpy as np


possibleDirections = [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1]
]



class Walker:
    def __init__(self,  gridSize, size=1, pos=None):
        self.dir = possibleDirections[np.random.choice(4)]
        self.size = size
        self.grid_size = gridSize
        self.pos = None
        self.is_moving = False
        if pos is None:
            self.pos = [int(np.ceil(gridSize[0]/2)) - 1, int(np.ceil(gridSize[1]/2)) - 1]
        else:
            self.pos = pos

    def move(self, offset):
        new_pos = np.add(self.pos, self.dir)
        if offset[0] <= new_pos[0] < self.grid_size[0] - offset[0] - 1 and offset[1] <= new_pos[1] < self.grid_size[1] - offset[1] - 1:
            self.pos = new_pos

    def change_dir(self):
        self.dir = possibleDirections[np.random.choice(4)]
