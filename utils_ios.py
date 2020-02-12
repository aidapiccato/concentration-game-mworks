import numpy as np
import pickle as pk

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


def get_block_metaparameters_ios():
    subject_id = int(getvar('subject_id'))
    sess_index = int(getvar('sess_index'))
    block_index = int(getvar('block_index'))
    n_pairs, grid, grid_dims, inv_grid, trials = generate_block(subject_id, sess_index, block_index)
    setvar('py_n_pairs', n_pairs)
    setvar('py_grid_dims', grid_dims)
    setvar('py_grid', grid)
    setvar('py_inv_grid', inv_grid)
    setvar('py_trials', trials)


########################################################################################################################

def get_block(subject_id, sess_index, block_index):
    curr_sess = get_session(subject_id, sess_index)
    curr_block_n_pairs = curr_sess.blocks[block_index]
    curr_block = Block(curr_block_n_pairs, subject_id, sess_index, block_index)
    return curr_block.n_pairs, curr_block.grid, curr_block.grid_dims, curr_block.inv_grid, curr_block.trials


def get_session(subject_id, sess_index):
    np.random.seed(subject_id)
    session = Session(subject_id, sess_index)
    return session


class Session(object):
    def __init__(self, subject_id, sess_index, ):
        seed = hash((subject_id, sess_index)) % (2 ** 32 - 1)
        blocks = np.tile(ALL_N_PAIRS, N_CONFIG_REPEATS)
        for i in range(N_CONFIG_REPEATS):
            np.random.seed(seed + i)
            blocks[i * len(ALL_N_PAIRS):i * len(ALL_N_PAIRS) + len(ALL_N_PAIRS)] = np.random.permutation(
                blocks[i * len(ALL_N_PAIRS):i * len(ALL_N_PAIRS) + len(ALL_N_PAIRS)])
        self.blocks = blocks


class Block(object):
    def __init__(self, n_pairs, subject_id, sess_index, block_index):
        self.seed = hash((subject_id, sess_index, block_index)) % (2 ** 32 - 1)
        self.n_pairs = n_pairs
        self.grid = np.repeat(np.arange(n_pairs), 2)
        self.grid_dims = GRID_DIMS[n_pairs]
        if self.grid_dims[0] % 2 != 0:
            self.grid = np.append(self.grid, n_pairs)
        np.random.seed(self.seed)
        img_ixs = 2 * np.repeat(np.random.choice(np.arange(MAX_N_PAIRS), size=(n_pairs, 1), replace=False), 2) \
                  + np.tile([0, 1], n_pairs)
        if self.grid_dims[0] % 2 != 0:
            np.random.seed(self.seed)
            oddball = np.random.choice(np.setdiff1d(np.arange(MAX_N_PAIRS), img_ixs))  # randomly choose an image
            img_ixs = np.append(img_ixs, oddball)  # that is not already a pair
        inv_grid = np.zeros(MAX_N_IMAGES) - 1  # to be oddball
        inv_grid[img_ixs] = np.argsort(self.grid)
        self.inv_grid = np.asarray(inv_grid, dtype=int)
        # choices
        if self.grid_dims[0] % 2 != 0:
            oddball = inv_grid[img_ixs[-1]]
            choices = np.setdiff1d(np.arange(n_pairs * 2 + 1), [oddball])
        else:
            choices = np.arange(n_pairs * 2)
        # trials
        np.random.seed(self.seed)
        self.trials = np.random.permutation(np.repeat(choices, N_CYCLES))

# def generate_block(subject_id, block_index):
#     # create unique seed for subject
#     seed = hash((subject_id, block_index)) % (2 ** 32 - 1)  # seed must be in this range
#     # list of grid sizes (generate using subject_id as seed)
#     np.random.seed(subject_id)
#     configs = np.tile(ALL_N_PAIRS, N_CONFIG_REPEATS)
#     # shuffling to insure that adjacent arrays are not of the same size
#     for i in range(N_CONFIG_REPEATS):
#         np.random.seed(subject_id)
#         configs[i * N_CONFIG_REPEATS:i * N_CONFIG_REPEATS + len(ALL_N_PAIRS)] = np.random.permutation(
#             configs[i * N_CONFIG_REPEATS:i * N_CONFIG_REPEATS + len(ALL_N_PAIRS)])
#
#     # select current block size using block index
#     n_pairs = configs[block_index]
#     # create grid
#     grid = np.repeat(np.arange(n_pairs), 2)
#     if np.isin(n_pairs, [4, 12]):  # will have one 'oddball' card
#         grid = np.append(grid, n_pairs)  # adding oddball index
#
#     np.random.seed(seed)
#     np.random.shuffle(grid)
#     grid_dims = CONFIGS[n_pairs]
#     # produce img_ixs
#     np.random.seed(seed)
#     img_ixs = 2 * np.repeat(np.random.choice(np.arange(MAX_N_PAIRS), size=(n_pairs, 1), replace=False), 2) \
#               + np.tile([0, 1], n_pairs)
#     # choosing oddball if relevant
#     if np.isin(n_pairs, [4, 12]):
#         np.random.seed(seed)
#         oddball = np.random.choice(np.setdiff1d(np.arange(MAX_N_PAIRS), img_ixs))  # randomly choose an image
#         img_ixs = np.append(img_ixs, oddball)  # that is not already a pair
#     # produce inv_grid
#     inv_grid = np.zeros(MAX_N_IMAGES) - 1  # to be oddball
#     inv_grid[img_ixs] = np.argsort(grid)
#     inv_grid = np.asarray(inv_grid, dtype=int)
#     # choices
#     if np.isin(n_pairs, [4, 12]):
#         oddball = inv_grid[img_ixs[-1]]
#         choices = np.setdiff1d(np.arange(n_pairs * 2 + 1), [oddball])
#     else:
#         choices = np.arange(n_pairs * 2)
#     # trials
#     np.random.seed(seed)
#     trials = np.random.permutation(np.repeat(choices, N_CYCLES))
#
#     return n_pairs, grid, grid_dims, inv_grid, trials
