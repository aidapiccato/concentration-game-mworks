import pickle as pk
from utils import MAX_N_PAIRS, MAX_N_IMAGES, N_CONFIG_REPEATS, ALL_N_PAIRS, N_CYCLES, CONFIGS, dir_path
import numpy as np

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

