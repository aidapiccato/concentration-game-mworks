import pickle as pk
import numpy as np
from constants import *


def generate_subject_meta(subject_id):
    """
    Generate set of blocks for a single subject
    """
    meta = []

    subject_fn = '%s/meta/subject_%s.pkl' % (dir_path, subject_id)

    for n_pairs in ALL_N_PAIRS:
        for _ in range(N_CONFIG_REPEATS):
            grid = np.repeat(np.arange(n_pairs), 2)
            if np.isin(n_pairs, [4, 12]):  # will have one 'oddball' card
                grid = np.append(grid, n_pairs)  # adding oddball index

            np.random.shuffle(grid)

            img_ixs = 2 * np.repeat(np.random.choice(np.arange(MAX_N_PAIRS), size=(n_pairs, 1), replace=False), 2) \
                      + np.tile([0, 1], n_pairs)  # randomly choose n_pair images

            if np.isin(n_pairs, [4, 12]):
                oddball = np.random.choice(np.setdiff1d(np.arange(MAX_N_PAIRS), img_ixs)) # randomly choose an image
                img_ixs = np.append(img_ixs, oddball)                                     # that is not already a pair
            inv_grid = np.zeros(MAX_N_IMAGES) - 1                                         # to be oddball
            inv_grid[img_ixs] = np.argsort(grid)
            inv_grid = np.asarray(inv_grid, dtype=int)

            if np.isin(n_pairs, [4, 12]):
                oddball = inv_grid[img_ixs[-1]]
                choices = np.setdiff1d(np.arange(n_pairs * 2 + 1), [oddball])
            else:
                choices = np.arange(n_pairs * 2)

            trials = np.random.permutation(np.repeat(choices, N_CYCLES))

            config = {'n_pairs': n_pairs, 'grid_dims': CONFIGS[n_pairs], 'grid': grid,
                      'inv_grid': inv_grid, 'trials': trials, 'img_ixs': img_ixs}

            meta.append(config)

    meta = np.asarray(meta)

    # repeatedly shuffling array until no consecutive blocks have the same grid size
    while np.any([meta[i]['n_pairs'] == meta[i - 1]['n_pairs'] or meta[i]['n_pairs'] == meta[i + 1]['n_pairs']
                  for i in range(1, len(meta) - 1)]):
        np.random.shuffle(meta)

    with open(subject_fn, 'wb') as f:
        pk.dump(meta, f)
