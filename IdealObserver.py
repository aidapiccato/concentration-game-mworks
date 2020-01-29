import numpy as np


class IdealObserver(object):

    def __init__(self, grid_dims, n_pairs):
        self.grid_dims = grid_dims
        self.n_imgs = grid_dims[0] * grid_dims[1]

        self.n_pairs = n_pairs

        self.grid = np.zeros(self.n_imgs) - 1

        self.card_a = None
        self.card_x = None
        self.img = None

    def reset_trial(self):
        self.card_a = None
        self.card_x = None
        self.img = None

    def _update_grid(self, a, img):
        self.grid[a] = img


    def _find_match(self, img):
        match = np.where(self.grid == img)[0]
        match = match[match != self.card_a]

        if len(match) == 0:
            unknowns = np.where(self.grid == -1)[0]
            card_b = np.random.choice(unknowns)
        else:
            card_b = match[0]
        return match

    # print_grid  b
    def choose(self, a, img):
        """
        Given card Axy, returns coordinates of pair
        :param a: location of card a
        :param img: image index of a
        :return:
        """

        self._update_grid(a, img)
        match = self._find_match(img)

        self.card_b = match
        return self.card_b

    def feedback(self, card_b, img):
        if img == self.img:
            self._update_grid(self.card_b, img)


