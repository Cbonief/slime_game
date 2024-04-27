from character import Moves, Move


def get_distance(this, end):
    return abs(end[0] - this[0]) + abs(end[1] - this[1])


def hash_from_list(X, gridSize):
    return X[0] + gridSize[0]*X[1]


def compare(X, hashY, gridSize):
    return hash_from_list(X, gridSize) == hashY


def compare_coordinates(X, Y, gridSize):
    return hash_from_list(X, gridSize) == hash_from_list(Y, gridSize)


def get_feasible_neighbors(current, grid, gridSize):
    neighbors = []

    for change in [[0, -1], [0, 1], [-1, 0], [1, 0]]:
        position_x = current[0] + change[0]
        position_y = current[1] + change[1]
        position = [position_x, position_y]
        feasible = True

        if grid[position_x][position_y] == 'f' and feasible:
            neighbors.append([position_x, position_y])
    return neighbors


def find_path_moves(start_position, final_position, grid, gridSize):
    move_list = Moves()

    hash_final_position = hash_from_list(final_position, gridSize)

    open_set = [start_position]

    closed_set = []
    came_from = {}

    g = {
        hash_from_list(start_position, gridSize): 0
    }
    h = {}
    f = {
        hash_from_list(start_position, gridSize): get_distance(start_position, final_position)
    }

    done = False
    closed_set_len = 0
    while len(open_set) > 0 and not done:
        len_open_set = len(open_set)
        winner = 0
        score_winner = f[hash_from_list(open_set[winner], gridSize)]
        for index in range(0, len_open_set):
            score = f[hash_from_list(open_set[index], gridSize)]
            if score <= score_winner:
                winner = index
                score_winner = score
        current = open_set[winner]
        hash_current = hash_from_list(current, gridSize)
        if compare(current, hash_final_position, gridSize):
            to_point = current
            key = hash_current
            while key in came_from:
                from_point = came_from[key]
                move_to_add = Move(direction=None, start=from_point, finish=to_point)
                move_list.add_move_begin(move_to_add)
                key = hash_from_list(from_point, gridSize)
                to_point = from_point
            done = True
        else:
            open_set.remove(current)
            closed_set.append(current)
            closed_set_len += 1

            neighbors = get_feasible_neighbors(current, grid, gridSize)
            for neighbor in neighbors:
                hash_neighbor = hash_from_list(neighbor, gridSize)
                on_closed_set = False
                on_open_set = False
                index = 0
                while not on_closed_set and index < closed_set_len:
                    if compare(closed_set[index], hash_neighbor, gridSize):
                        on_closed_set = True
                    index += 1
                index = 0
                while not on_open_set and index < len(open_set):
                    if compare(open_set[index], hash_neighbor, gridSize):
                        on_open_set = True
                    index += 1

                if not on_closed_set:
                    temp_g = g[hash_current] + 1
                    if on_open_set and temp_g < g[hash_neighbor]:
                        g[hash_neighbor] = temp_g
                    else:
                        g[hash_neighbor] = temp_g
                        open_set.append(neighbor)

                    h[hash_neighbor] = get_distance(neighbor, final_position)
                    f[hash_neighbor] = h[hash_neighbor] + g[hash_neighbor]
                    came_from[hash_neighbor] = current
    return move_list