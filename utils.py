import numpy as np
import pickle as pk

MAX_N_IMAGES = 36
MAX_N_PAIRS = 18

CONFIGS = { # mapping number of pairs to possible configurations
    2: [2, 2],
    8: [4, 4],
    18: [6, 6]
}
ALL_N_PAIRS = [2, 8, 18] # possible number of pairs in a configuration
N_CONFIG_REPEATS = 4 # number of times each configuration is repeated (each time with unique image layout)
N_CYCLES = 3
username = 'aidapiccato'
# username = 'apiccato'

dir_path = '/Users/%s/PyCharmProjects/concentration/concentration-game-mworks' % username

subject_id = getvar('subject_id')

subject_fn = '%s/meta/subject_%s.pkl' % (dir_path, subject_id)

with open(subject_fn, 'rb') as f:
    subject_meta = pk.load(f)

def get_block_metaparameters():
    block_index = int(getvar('block_index'))
    config = subject_meta[block_index]
    setvar('py_n_pairs', config['n_pairs'])
    setvar('py_grid_dims', np.asarray(config['grid_dims'], dtype=int))
    setvar('py_feedback', int(config['feedback']))
    setvar('py_grid', np.asarray(config['grid'], dtype=int))
    setvar('py_inv_grid', np.asarray(config['inv_grid'], dtype=int))

def get_trial_metaparameters():
    """
    Returns card_a for current trial
    """
    trial_index = int(getvar('trial_index'))
    block_index = int(getvar('block_index'))
    config = subject_meta[block_index]
    card_a = config['trials'][trial_index]
    setvar('py_card_a', card_a)

########################################################################################################################

def generate_subject_meta(subject_id):
    """
    Generate set of blocks for a single subject
    """
    meta = []

    subject_fn = '%s/meta/subject_%s.pkl' % (dir_path, subject_id)

    for n_pairs in ALL_N_PAIRS:
        for _ in range(N_CONFIG_REPEATS):
            grid = np.repeat(np.arange(n_pairs), 2)
            np.random.shuffle(grid)

            img_ixs = 2 * np.repeat(np.random.choice(np.arange(MAX_N_PAIRS), size=(n_pairs, 1), replace=False), 2) \
                      + np.tile([0, 1], n_pairs)  ## randomly choose n_pair images

            inv_grid = np.zeros(MAX_N_IMAGES) - 1
            inv_grid[img_ixs] = np.argsort(grid)
            inv_grid = np.asarray(inv_grid, dtype=int)

            trials = np.random.permutation(np.repeat(np.arange(n_pairs * 2), N_CYCLES))

            config = {'n_pairs': n_pairs, 'grid_dims': CONFIGS[n_pairs], 'grid': grid,
                      'inv_grid': inv_grid, 'feedback': 0, 'trials': trials}

            meta.append(config)

    meta = np.asarray(meta)

    np.random.shuffle(meta)

    with open(subject_fn, 'wb') as f:
        pk.dump(meta, f)







