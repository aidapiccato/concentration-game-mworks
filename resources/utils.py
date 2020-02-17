import numpy as np
import pickle as pkl
import datetime

N_SESSIONS = 10
MAX_N_IMAGES = 25
MAX_N_PAIRS = 12
GRID_DIMS = {
    2: [2, 2],
    4: [3, 3],
    8: [4, 4],
    12: [5, 5],
}
ALL_N_PAIRS = [2, 4, 8, 12]
N_CONFIG_REPEATS = 10
N_CYCLES = 4
version = 1


# def add_sess():
#     subject_id = int(getvar('subject_id'))
#     sess_index = int(getvar('sess_index'))
#     sessions = subject_sess[subject_sess.subject_id == subject_id]
#     session = {'subject_id': subject_id, 'date': datetime.datetime.now().strftime('%x'), 'sess_index': sess_index}
#     sessions = sessions.append(session, ignore_index=True)
#     with open(subject_sess_dirpath, 'wb') as g:
#         pkl.dump(sessions, g)


def get_block_metaparameters():
    subject_id = int(getvar('subject_id'))
    sess_index = int(getvar('sess_index'))
    block_index = int(getvar('block_index'))
    n_pairs, grid, grid_dims, n_images, trials = get_block(subject_id, sess_index, block_index)
    setvar('py_n_pairs', n_pairs)
    setvar('py_grid_dims', grid_dims)
    setvar('py_grid', grid)
    setvar('py_n_images', n_images)
    setvar('py_trials', trials)


########################################################################################################################


def get_block(subject_id, sess_index, block_index):
    curr_sess = get_session(subject_id, sess_index)
    curr_block_n_pairs = curr_sess.blocks[block_index]
    curr_block = Block(curr_block_n_pairs, subject_id, sess_index, block_index)
    return curr_block.n_pairs, curr_block.grid, curr_block.grid_dims, curr_block.n_images, curr_block.trials


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

        self.grid = np.arange(block_index * (MAX_N_PAIRS + 1), (block_index + 1) * (MAX_N_PAIRS + 1), step=1)
        self.grid_dims = GRID_DIMS[n_pairs]
        self.n_images = self.n_pairs * 2 + (self.grid_dims[0] % 2) * 1
        self.grid = np.repeat(self.grid, 2)
        self.grid = self.grid[:self.n_images]
        oddball = self.grid[-1]

        np.random.seed(self.seed)
        np.random.shuffle(self.grid)

        choices = np.arange(self.n_images)

        if self.grid_dims[0] % 2 != 0:
            choices = np.where(self.grid != oddball)[0]

        np.random.seed(self.seed)
        self.trials = np.random.permutation(np.repeat(choices, N_CYCLES))
