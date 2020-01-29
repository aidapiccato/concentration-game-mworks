import numpy as np


class IdealObserver(object):

    def __init__(self, grid_dims, n_pairs):
        self.grid_dims = grid_dims
        self.n_pairs = n_pairs
        self.grid = np.zeros(self.grid_dims)

    def update_grid(self, x, y, img):
        self.grid[x, y] = img


    def choose(self, x, y, img):
        """
        Given card Axy, returns coordinates of pair
        :param x: x-coordinate of A
        :param y: y-coordinate of A
        :param img: image index of a
        :return:
        """

        self.update_grid(x, y, img)

        match = np.where(self.grid == img)[0]

        match = match[match != [x, y]]