from walker import Walker
import numpy as np
from path_finding import hash_from_list

positions = (
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1)
)


def create_level(gridSize, off_set, startingWalkers=1, chanceWalkerChangeDir=0.5, chanceWalkerSpawn=0.05, chanceWalkerDestroy=0.05, maxWalkers=10, percentToFill=0.2):
    grid = np.zeros((gridSize[0], gridSize[1]), dtype=str)
    for i in range(0, gridSize[0]):
        for j in range(0, gridSize[1]):
            grid[i][j] = 'e'

    [grid, feasible_positions] = create_floors(gridSize, off_set, grid, startingWalkers=1, chanceWalkerChangeDir=0.5, chanceWalkerSpawn=0.05, chanceWalkerDestroy=0.05, maxWalkers=10, percentToFill=0.2)
    grid = create_walls(gridSize, grid)
    [grid, door_direction] = create_door(gridSize, grid)
    return [grid, door_direction, feasible_positions]


def create_floors(gridSize, off_set, grid, startingWalkers=1, chanceWalkerChangeDir=0.5, chanceWalkerSpawn=0.05, chanceWalkerDestroy=0.05, maxWalkers=10, percentToFill=0.2):
    walkers = []
    for n in range(0, startingWalkers):
        walkers.append(Walker(gridSize))

    finished = False
    iteration = 0
    feasible_positions = {}
    floor_count = 0
    while not finished and iteration < 100000:
        for walker in walkers:
            pos = walker.pos
            for change_i in [0, 1]:
                for change_j in [0, 1]:
                    i = pos[0] + change_i
                    j = pos[1] + change_j
                    grid[i][j] = 'f'
                    coordinates = [i, j]
                    if hash_from_list(coordinates, gridSize) not in feasible_positions:
                        floor_count += 1
                        feasible_positions[hash_from_list(coordinates, gridSize)] = coordinates

        percentage = floor_count/(gridSize[0]*gridSize[1])
        if percentage > percentToFill:
            finished = True

        if not finished:
            number_of_walkers = len(walkers)
            destroyed = False
            index = 0
            while index < number_of_walkers and not destroyed:
                value = np.random.random()
                if number_of_walkers > 1 and value < chanceWalkerDestroy:
                    walkers.pop(index)
                    destroyed = True
                    number_of_walkers -= 1
                index += 1

            for walker in walkers:
                value = np.random.random()
                if value < chanceWalkerChangeDir:
                    walker.change_dir()

            for index in range(0, number_of_walkers):
                value = np.random.random()
                if value < chanceWalkerSpawn and number_of_walkers < maxWalkers:
                    new_walker = Walker(gridSize, np.random.choice([1, 2]), walkers[index].pos)
                    walkers.append(new_walker)

            for walker in walkers:
                walker.move(off_set)
        iteration += 1
    print('Done')
    return [grid, feasible_positions]


def create_walls(gridSize, grid):
    for i in range(0, gridSize[0]):
        for j in range(0, gridSize[1]):
            if grid[i][j] == 'f':
                for position in positions:
                    if grid[i+position[0]][j+position[1]] == 'e':
                        grid[i+position[0]][j+position[1]] = 'w'
    return grid


def create_door(gridSize, grid):
    possible_spots = []
    number_of_possible_spots = 0
    for i in range(0, gridSize[0]):
        for j in range(0, gridSize[1]):
            if grid[i][j] == 'w':
                door_direction = {
                    'Up': True,
                    'Down': True,
                    'Left': True,
                    'Right': True
                }
                # Left side
                if i == 0 and j != 0 and j != gridSize[1] - 1:
                    door_direction['Up'] = False
                    door_direction['Down'] = False
                    door_direction['Left'] = False
                    if grid[i][j+1] == 'w' and grid[i][j-1] == 'w':
                        for n in [-1, 0, 1]:
                            if not (grid[i + 1][j + n] == 'f'):
                                door_direction['Right'] = False
                    else:
                        door_direction['Right'] = False
                # Right side
                elif i == gridSize[0] - 1 and j != 0 and j != gridSize[1] - 1:
                    door_direction['Up'] = False
                    door_direction['Down'] = False
                    door_direction['Right'] = False
                    if grid[i][j + 1] == 'w' and grid[i][j - 1] == 'w':
                        for n in [-1, 0, 1]:
                            if not (grid[i - 1][j + n] == 'f'):
                                door_direction['Left'] = False
                    else:
                        door_direction['Left'] = False
                # Top side
                elif j == 0 and i != 0 and i != gridSize[0] - 1:
                    door_direction['Up'] = False
                    door_direction['Left'] = False
                    door_direction['Right'] = False
                    if grid[i+1][j] == 'w' and grid[i-1][j] == 'w':
                        for n in [-1, 0, 1]:
                            if not (grid[i + n][j + 1] == 'f'):
                                door_direction['Down'] = False
                    else:
                        door_direction['Down'] = False
                # Down side
                elif j == gridSize[1] - 1 and i != 0 and i != gridSize[0] - 1:
                    door_direction['Down'] = False
                    door_direction['Left'] = False
                    door_direction['Right'] = False
                    if grid[i+1][j] == 'w' and grid[i-1][j] == 'w':
                        for n in [-1, 0, 1]:
                            if not (grid[i + n][j - 1] == 'f'):
                                door_direction['Up'] = False
                    else:
                        door_direction['Up'] = False
                else:
                    if grid[i][j+1] == 'w' and grid[i][j-1] == 'w':
                        for n in [-1, 0, 1]:
                            if not (grid[i+1][j+n] == 'e' and grid[i-1][j+n] == 'f'):
                                door_direction['Left'] = False
                            if not (grid[i-1][j+n] == 'e' and grid[i+1][j+n] == 'f'):
                                door_direction['Right'] = False
                            if not (grid[i+n][j+1] == 'e' and grid[i+n][j-1] == 'f'):
                                door_direction['Up'] = False
                            if not (grid[i+n][j-1] == 'e' and grid[i+n][j+1] == 'f'):
                                door_direction['Down'] = False
                    else:
                        door_direction['Up'] = False
                        door_direction['Down'] = False
                        door_direction['Left'] = False
                        door_direction['Right'] = False
                for key in door_direction:
                    if door_direction[key]:
                        possible_spots.append(
                            {
                                'pos': [i, j],
                                'dir': key
                            }
                        )
                        number_of_possible_spots += 1

    spot_index = np.random.choice(number_of_possible_spots-1)
    grid[possible_spots[spot_index]['pos'][0]][possible_spots[spot_index]['pos'][1]] = 'd'
    door_direction = possible_spots[spot_index]['dir']
    return [grid, door_direction]