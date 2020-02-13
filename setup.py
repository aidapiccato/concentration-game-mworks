import os
import numpy as np

N_SESSIONS = 10
MAX_N_IMAGES = 36
MAX_N_PAIRS = 18
GRID_DIMS = {
    2: [2, 2],
    4: [3, 3],
    8: [4, 4],
    12: [5, 5],
}
ALL_N_PAIRS = [2, 4, 8, 12]
N_CONFIG_REPEATS = 10
N_CYCLES = 4
N_IMAGES_TOTAL = 3000
N_IMAGES_PER_SESSION = MAX_N_IMAGES * N_CONFIG_REPEATS * len(ALL_N_PAIRS)

def populate(subject_id, sess_index):
    seed = hash((subject_id)) % 2**32 - 1
    images = np.arange(N_IMAGES_TOTAL)
    np.random.seed(seed)
    np.random.shuffle(images)
    sess_images = images[sess_index * N_IMAGES_PER_SESSION : (sess_index + 1) * N_IMAGES_PER_SESSION]
    
