import numpy as np
import pickle as pkl
import datetime
import json


VERSION = 1
dir = ''
# dir = '/Users/apiccato/PycharmProjects/concentration/concentration-game-mworks/'
json_path = dir + 'resources/config.json'



with open(json_path) as f:
    config = json.load(f)
n_sessions = config["n_sessions"]
max_n_images = config["max_n_images"]
max_n_pairs = config["max_n_pairs"]
all_n_pairs = config["all_n_pairs"]
n_config_repeats = config["n_config_repeats"]
n_cycles = config["n_cycles"]
version = config["version"]


def get_session_metaparameters():
    with open(json_path) as f:
        config = json.load(f)
    setvar('py_n_cycles', config['n_cycles'])
    setvar('py_n_configs', len(config['all_n_pairs']))
    setvar('py_n_cards_max', config['max_n_images'])
    setvar('py_n_config_repeats', config['n_config_repeats'])

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
    setvar('py_n_trials', len(trials))


########################################################################################################################


def odd_block(n_pairs):
    root = np.sqrt(n_pairs * 2)
    return int(root + 0.5) ** 2 != (n_pairs * 2)

def get_block(subject_id, sess_index, block_index):
    curr_sess = get_session(subject_id, sess_index)

    curr_block_n_pairs = curr_sess.blocks[block_index]
    curr_block = Block(curr_block_n_pairs, subject_id, sess_index, block_index, curr_sess.n_imgs_cum[block_index])
    return curr_block.n_pairs, curr_block.grid, curr_block.grid_dims, curr_block.n_images, curr_block.trials


def get_session(subject_id, sess_index):
    np.random.seed(subject_id)
    session = Session(subject_id, sess_index)
    return session


class Session(object):
    def __init__(self, subject_id, sess_index, ):
        seed = hash((subject_id, sess_index)) % (2 ** 32 - 1)
        blocks = np.tile(all_n_pairs, n_config_repeats)
        for i in range(n_config_repeats):
            block_range = np.arange(start=i * len(all_n_pairs), stop=i * len(all_n_pairs) + len(all_n_pairs))
            np.random.seed(seed + i)
            blocks[block_range] = np.random.permutation(blocks[block_range])
        self.blocks = blocks
        n_imgs_per_block = np.asarray([block + (odd_block(block)) * 1 for block in blocks])
        n_imgs_per_block = np.concatenate([[0], n_imgs_per_block])
        self.n_imgs_cum = np.cumsum(n_imgs_per_block)


class Block(object):
    def __init__(self, n_pairs, subject_id, sess_index, block_index, img_index):
        self.seed = hash((subject_id, sess_index, block_index)) % (2 ** 32 - 1)
        self.n_pairs = n_pairs
        self.n_images = self.n_pairs * 2
        if odd_block(n_pairs):
            self.n_images = self.n_images + 1
        self.grid = np.arange(img_index, img_index + self.n_images, step=1)
        root = np.sqrt(n_pairs * 2)
        if odd_block(n_pairs):
            root = np.sqrt(n_pairs * 2 + 1)
        self.grid_dims = [int(root), int(root)]
        self.grid = np.repeat(self.grid, 2)
        self.grid = self.grid[:self.n_images]
        oddball = self.grid[-1]

        np.random.seed(self.seed)
        np.random.shuffle(self.grid)

        choices = np.arange(self.n_images)

        if self.grid_dims[0] % 2 != 0:
            choices = np.where(self.grid != oddball)[0]

        np.random.seed(self.seed)
        self.trials = np.random.permutation(np.repeat(choices, n_cycles))
