import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/Library/Application Support/MWorks/Scripting/Python')
from mworks.data import MWKFile

# sync values
ITI = 1
TRIAL_INIT = 2
FLIP_CARD_A = 3
FLIP_CARD_B = 4
FEEDBACK = 5
TRIAL_END = 6

max_grid_dims = [5, 5]

username = 'apiccato'
dir_path = '/Users/%s/PyCharmProjects/concentration/concentration-game-mworks' % username
fpath = '/Users/%s/Documents/MWorks/Data' % username


class ConcentrationBehavior(object):
    """
    Class to unpack and process behavioral data from Concentration task.
    """

    def __init__(self, fns,
                 codenames=None
                 ):
        """
        :param fns: Filenames of .mwk2 files containing event stream
        :param codenames: Names of vars to extract from event stream
        """
        if codenames is None:
            codenames = ['card_b', 'card_a', 'grid', 'grid_dims', 'inv_grid', 'n_pairs', 'block_index',
                         'trial_index', 'feedback_dur', 'trial_in_block_index']

        self.fns = fns
        self.codenames = codenames
        scalar, start_sync_t, end_sync_t, n_trials = self.get_trials()
        self.scalar, self.start_sync_t, self.end_sync_t, self.n_trials = scalar, start_sync_t, end_sync_t, n_trials
        self.set_card_c()  # sets card_c column scalar
        self.set_success()  # sets success column in scalar
        self.set_spatial()  # gets spatial information for each trial
        self.set_views()  # creates views dataframe
    #     self.spatial = self.get_spatial()

    def set_views(self):
        views = {'card': [], 'trial_in_block_index': [], 'trial_index': [], 'time': [], 'block_index': []}
        for trial_index, trial in self.scalar.iterrows():
            views['card'].append(trial.card_a)
            views['time'].append(trial.card_a_t)
            views['trial_in_block_index'].append(trial.trial_in_block_index)
            views['trial_index'].append(trial.trial_index)
            views['block_index'].append(trial.block_index)

            if
    def set_spatial(self):
        """
        :return: Dataframe with spatial information for each trial
        """
        self.spatial = pd.DataFrame({})
        self.spatial['dist_a_b'] = self.scalar.apply(lambda t: self.get_dist(t.card_a, t.card_b, t.grid_dims), axis=1)
        self.spatial['dist_a_c'] = self.scalar.apply(lambda t: self.get_dist(t.card_a, t.card_c, t.grid_dims), axis=1)
        self.spatial['dist_b_c'] = self.scalar.apply(lambda t: self.get_dist(t.card_b, t.card_c, t.grid_dims), axis=1)


    def get_dist(self, card_a, card_b, grid_dims):
        card_a_loc = np.asarray([np.floor(card_a / grid_dims[1]), card_a % grid_dims[1]])
        card_b_loc = np.asarray([np.floor(card_b / grid_dims[1]), card_b % grid_dims[1]])
        max_dist = np.linalg.norm(max_grid_dims)
        return np.linalg.norm(card_a_loc - card_b_loc)/max_dist

    def set_success(self):
        self.scalar['success'] = self.scalar.apply(lambda t: t.card_b == t.card_c, axis=1)

    def set_card_c(self):
        def get_c(trial):
            match = np.where(np.asarray(trial.grid) == trial.grid[trial.card_a])[0]
            return match[match != trial.card_a][0]

        self.scalar['card_c'] = self.scalar.apply(lambda t: get_c(t), axis=1)


    def get_trials(self):
        """
        Returns times of trial inits, trial ends, and number of trials
        :return: Array of trial start times, array of trial end times, number of trials
        """
        n_trials, start_sync_t, end_sync_t = 0, np.asarray([]), np.asarray([])
        scalar = pd.DataFrame()
        for fn in self.fns:
            f = MWKFile('%s/%s' % (fpath, fn))
            f.open()
            fn_start_sync_t = self.get_sync_t(f, TRIAL_INIT)
            fn_end_sync_t = self.get_sync_t(f, TRIAL_END)
            fn_start_sync_t = fn_start_sync_t[:len(fn_end_sync_t)]
            start_sync_t = np.concatenate((start_sync_t, fn_start_sync_t))
            end_sync_t = np.concatenate((end_sync_t, fn_end_sync_t))
            fn_unpack = self.unpack(f, fn_start_sync_t, fn_end_sync_t)
            scalar = pd.concat((scalar, fn_unpack))
            f.close()

        n_trials = len(start_sync_t)

        scalar = pd.DataFrame(scalar)

        scalar = scalar.sort_values(by=['block_index', 'trial_in_block_index'])

        scalar.trial_index = np.arange(n_trials)

        return scalar, start_sync_t, end_sync_t, n_trials

    def unpack(self, f, start_sync_t, end_sync_t):
        """
        Extracts data for codenames for each trial
        :return:
        """
        unpacked = {}
        for c in self.codenames:
            unpacked[c] = []
        n_trials = len(start_sync_t)
        for t in range(n_trials):
            start_t, end_t = np.long(start_sync_t[t]), np.long(end_sync_t[t])
            trial_events = f.get_events(codes=self.codenames, time_range=[start_t, end_t])
            trial_events = np.asarray([[e.code, e.time, e.data] for e in trial_events])
            for ci, c in enumerate(self.codenames):
                code = f.reverse_codec[c]
                code_events = trial_events[np.where(trial_events[:, 0] == code)[0], 2]
                if len(code_events) == 0:
                    code_events = [None]
                unpacked[c].append(code_events[0])
        unpacked = pd.DataFrame(unpacked)
        return unpacked

    @staticmethod
    def get_sync_t(f, sync_code):
        """
        Returns array of events for setting of sync variable to sync_code
        :param f: MWKFile object
        :param sync_code: String array for events
        :return: events: Array of events, each event represented as 2-element array [data, time]
        """
        events = f.get_events(codes=['sync'])
        events = np.asarray([[e.data, e.time] for e in events])
        events = events[np.where(events[:, 0] == sync_code)[0], 1]
        return events
