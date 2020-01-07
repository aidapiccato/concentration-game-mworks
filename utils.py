import numpy as np

def get_config_metaparameters():
    n_pairs = 8
    grid_dims = (4, 4)
    feedback = False
    grid = np.repeat(np.arange(n_pairs), 2)
    np.random.shuffle(grid)
    grid = np.reshape(grid, grid_dims)
    setvar('py_n_pairs', n_pairs)
    setvar('py_grid_dims', grid_dims)
    setvar('py_feedback', feedback)
    setvar('py_grid', grid)

def get_trial_metaparameters ():
    n_pairs = 8
    setvar('py_card_a', (np.random.randint(n_pairs * 2)))
