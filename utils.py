import numpy as np

MAX_N_IMAGES = 16
MAX_N_PAIRS = 8

def get_config_metaparameters():
    n_pairs = 2
    img_ixs = 2 * np.repeat(np.random.choice(np.arange(MAX_N_PAIRS), size=(n_pairs, 1), replace=False), 2)  + np.tile([0, 1], n_pairs)
    grid_dims = (2, 2)
    feedback = False
    grid = np.repeat(np.arange(n_pairs), 2)
    np.random.shuffle(grid)
    inv_grid = np.zeros(MAX_N_IMAGES) - 1
    inv_grid[img_ixs] = np.argsort(grid)
    setvar('py_n_pairs', n_pairs)
    setvar('py_grid_dims', grid_dims)
    setvar('py_feedback', feedback)
    setvar('py_grid', grid)
    setvar('py_inv_grid', inv_grid)

def get_trial_metaparameters ():
    n_pairs = 2
    setvar('py_card_a', (np.random.randint(n_pairs * 2)))
