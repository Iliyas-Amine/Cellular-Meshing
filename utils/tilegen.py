import numpy as np, random
from utils.config import (GRID_SIZE, INITIAL_SEEDS, UPDATE_ITERATIONS, NEIGHBOR_ACTIVATION_FACTOR)

def _get_neighbors(x, y):
    return [
        (x + dx, y + dy)
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1]
        if not (dx == 0 and dy == 0)
        and 0 <= x + dx < GRID_SIZE
        and 0 <= y + dy < GRID_SIZE
    ]

def _update_matrix(matrix):
    new_matrix = matrix.copy()
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            current_value = matrix[x, y]
            n = sum([matrix[x, y] for x, y in _get_neighbors(x, y)])
            if current_value == 0 and random.uniform(0, 1) < n*NEIGHBOR_ACTIVATION_FACTOR:
                new_matrix[x, y] = 1
    return new_matrix

def _gen_pop():
    env = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.int8)
    for _ in range(INITIAL_SEEDS):
        env[random.randint(0,GRID_SIZE-1), random.randint(0,GRID_SIZE-1)] = 1
    for _ in range(UPDATE_ITERATIONS):
        env = _update_matrix(env)
    return env