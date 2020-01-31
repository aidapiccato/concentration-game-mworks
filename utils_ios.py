import numpy as np
import pickle as pk

MAX_N_IMAGES = 36
MAX_N_PAIRS = 18

CONFIGS = { # mapping number of pairs to possible configurations
    2: [2, 2],
    4: [3, 3],
    8: [4, 4],
    12: [5, 5],
    # 18: [6, 6]
}

ALL_N_PAIRS = [2, 4, 8, 12] # possible number of pairs in a configuration; removed 18

N_CONFIG_REPEATS = 8 # number of times each configuration is repeated (each time with unique image layout)

N_CYCLES = 4

subject_id = getvar('subject_id')

def get_block_metaparameters_ios():
    block_index = int(getvar('block_index'))
    n_pairs, grid, grid_dims, inv_grid, trials = generate_block(subject_id, block_index)
    setvar('py_n_pairs', n_pairs)
    setvar('py_grid_dims', grid_dims)
    setvar('py_grid', grid)
    setvar('py_inv_grid', inv_grid)
    setvar('py_trials', trials)


########################################################################################################################

def generate_block(subject_id, block_index):
    # create unique seed for subject
    seed = hash((subject_id, block_index)) % (2**32 - 1) # seed must be in this range
    # list of grid sizes (generate using subject_id as seed)
    np.random.seed(subject_id)
    configs = np.tile(ALL_N_PAIRS, N_CONFIG_REPEATS)
    # shuffling to insure that adjacent arrays are not of the same size
    for i in range(N_CONFIG_REPEATS):
        np.random.seed(subject_id)
        configs[i*N_CONFIG_REPEATS:i*N_CONFIG_REPEATS+len(ALL_N_PAIRS)] = np.random.permutation(
            configs[i*N_CONFIG_REPEATS:i*N_CONFIG_REPEATS+len(ALL_N_PAIRS)])

    # select current block size using block index
    n_pairs = configs[block_index]
    # create grid
    grid = np.repeat(np.arange(n_pairs), 2)
    if np.isin(n_pairs, [4, 12]):  # will have one 'oddball' card
        grid = np.append(grid, n_pairs)  # adding oddball index

    np.random.seed(seed)
    np.random.shuffle(grid)
    grid_dims = CONFIGS[n_pairs]
    # produce img_ixs
    np.random.seed(seed)
    img_ixs = 2 * np.repeat(np.random.choice(np.arange(MAX_N_PAIRS), size=(n_pairs, 1), replace=False), 2) \
        + np.tile([0, 1], n_pairs)
    # choosing oddball if relevant
    if np.isin(n_pairs, [4, 12]):
        np.random.seed(seed)
        oddball = np.random.choice(np.setdiff1d(np.arange(MAX_N_PAIRS), img_ixs))  # randomly choose an image
        img_ixs = np.append(img_ixs, oddball)  # that is not already a pair
    # produce inv_grid
    inv_grid = np.zeros(MAX_N_IMAGES) - 1  # to be oddball
    inv_grid[img_ixs] = np.argsort(grid)
    inv_grid = np.asarray(inv_grid, dtype=int)
    # choices
    if np.isin(n_pairs, [4, 12]):
        oddball = inv_grid[img_ixs[-1]]
        choices = np.setdiff1d(np.arange(n_pairs * 2 + 1), [oddball])
    else:
        choices = np.arange(n_pairs * 2)
    # trials
    np.random.seed(seed)
    trials = np.random.permutation(np.repeat(choices, N_CYCLES))

    return n_pairs, grid, grid_dims, inv_grid, trials










