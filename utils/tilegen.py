import numpy as np, random

def _get_neighbors(x, y):
    return [
        (x + dx, y + dy)
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1]
        if not (dx == 0 and dy == 0)
        and 0 <= x + dx < 64
        and 0 <= y + dy < 64
    ]

def _update_matrix(matrix):
    new_matrix = matrix.copy()
    for x in range(64):
        for y in range(64):
            current_value = matrix[x, y]
            n = sum([matrix[x, y] for x, y in _get_neighbors(x, y)])
            if current_value == 0 and random.uniform(0, 1) < n*0.11:
                new_matrix[x, y] = 1
    return new_matrix

def _gen_pop():
    env = np.zeros((64, 64), dtype=np.int8)
    for _ in range(5):
        env[random.randint(0,63), random.randint(0,63)] = 1
    for _ in range(25):
        env = _update_matrix(env)
    return env