import numpy as np

MAX_N_IMAGES = 16
MAX_N_PAIRS = 8
CONFIGS = { # mapping number of pairs to possible configurations
    2: [[2, 2]],
    4: [[2, 4]],
    8: [[4, 4], [2, 8]]
}
ALL_N_PAIRS = [2, 4, 8] # possible number of pairs in a configuration

def get_config_metaparameters():

    n_pairs = np.random.choice(ALL_N_PAIRS)
    img_ixs = 2 * np.repeat(np.random.choice(np.arange(MAX_N_PAIRS), size=(n_pairs, 1), replace=False), 2) \
              + np.tile([0, 1], n_pairs)
    grid_dims = CONFIGS[n_pairs][np.random.randint(len(CONFIGS[n_pairs]))]
    np.random.shuffle(grid_dims)
    grid = np.repeat(np.arange(n_pairs), 2)
    np.random.shuffle(grid)
    inv_grid = np.zeros(MAX_N_IMAGES) - 1
    inv_grid[img_ixs] = np.argsort(grid)
    inv_grid = np.asarray(inv_grid, dtype=int)
    feedback = True
    setvar('py_n_pairs', n_pairs)
    setvar('py_grid_dims', grid_dims)
    setvar('py_feedback', feedback)
    setvar('py_grid', grid)
    setvar('py_inv_grid', inv_grid)

def get_trial_metaparameters ():
    n_pairs = int(getvar('n_pairs'))
    feedback = getvar('feedback')
    if (feedback):
        flipped = np.asarray(getvar('flipped'), dtype=int)
        flipped = flipped[:n_pairs * 2]
        not_flipped = np.where(flipped == 0)[0]
        if (len(not_flipped) == 0):
            card_a = -1
        else:
            card_a = np.random.choice(not_flipped)
    else:
        card_a = np.random.randint(n_pairs * 2)
    setvar('py_card_a', card_a)
