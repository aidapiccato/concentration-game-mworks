MAX_N_IMAGES = 36
MAX_N_PAIRS = 18

CONFIGS = { # mapping number of pairs to possible configurations
    2: [2, 2],
    4: [3, 3],
    8: [4, 4],
    12: [5, 5],
    18: [6, 6]
}

ALL_N_PAIRS = [2, 4, 8, 12, 18] # possible number of pairs in a configuration

N_CONFIG_REPEATS = 4 # number of times each configuration is repeated (each time with unique image layout)

N_CYCLES = 3

username = 'aidapiccato'
# username = 'apiccato'

dir_path = '/Users/%s/PyCharmProjects/concentration/concentration-game-mworks' % username
