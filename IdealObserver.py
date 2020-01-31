import numpy as np


class IdealObserver(object):

    def __init__(self, grid_dims, n_pairs):
        self._grid_dims = grid_dims
        self.n_imgs = grid_dims[0] * grid_dims[1]

        self.n_pairs = n_pairs

        self._grid = np.zeros(self.n_imgs) - 1

        self.explained_away = [[] for img in range(self.n_imgs)]  ## array of positions which each image cannot be in
        self.card_a = None
        self.card_x = None
        self.img = None

    def reset_trial(self):
        self.card_a = None
        self.card_x = None
        self.img = None

    def _update_grid(self, a, img):
        """
        Set grid position a to image img
        """
        self._grid[a] = img

    def _unknowns(self):
        """
        List of grid positions for which image is unknown. Obs. chooses randomly from these when image is unknown.
        :return:
        """
        return np.where(self._grid == -1)[0]

    def _find_match(self, img):
        """
        Returns grid positions containing image.
        :param img: image index
        :return:
        """
        return set(np.where(self._grid == img)[0])

    def grid(self):
        grid_copy = np.zeros(shape=self._grid.shape, dtype=str)
        grid_copy[self._grid == -1.0] = '?'
        grid_copy[self._grid != -1.0] = self._grid[self._grid != -1.0]
        return grid_copy.reshape(self._grid_dims)

    def choice(self, a, img):
        """
        Given card Axy, returns coordinates of pair
        :param a: location of card a
        :param img: image index of a
        :return:
        """
        # save card a to correct position

        self._update_grid(a, img)
        match = self._find_match(img)
        match = match - {a}
        if len(match) == 0:
            return np.random.choice(self._unknowns())
        return match.pop()

    def feedback(self, b, img):
        """
        Updates grid given correct image stored at location b
        """
        self._update_grid(b, img)






