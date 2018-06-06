import numpy as np

import torch
from torch.utils.data import Dataset

class SARSDataset(Dataset):
    """
    Container class for state, action, reward, new state observations.
    """

    def __init__(self, sars_data=None):
        """

        :param sars_data: [{'prev_state': array, 'action': array, 'reward': array, 'new_state'}, ... ]
        """
        self.prev_states = self._dict_to_nparray(sars_data, 'prev_state') if sars_data is not None else None
        self.actions = self._dict_to_nparray(sars_data, 'action') if sars_data is not None else None
        self.rewards = self._dict_to_nparray(sars_data, 'reward') if sars_data is not None else None
        self.new_states = self._dict_to_nparray(sars_data, 'new_state') if sars_data is not None else None

    def __len__(self):
        return len(self.prev_states) if self.prev_states is not None else 0

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return torch.FloatTensor(np.concatenate((self.prev_states[idx], self.actions[idx], self.rewards[idx], self.new_states[idx]), axis=1))
        else:
            return torch.FloatTensor(np.concatenate((self.prev_states[idx], self.actions[idx], self.rewards[idx], self.new_states[idx]), axis=0))

    def _dict_to_nparray(self, sars_data, key):
        if len(sars_data) < 1:
            return np.array([])

        dim = len(sars_data[0][key]) if sars_data[0][key] is list else 1
        res = np.zeros((len(sars_data), dim))
        for sars_idx, sars in enumerate(sars_data):
            res[sars_idx] = sars[key] if type(sars[key]) is not list else np.array(sars[key])
        return res

    def append(self, sars_data):
        """
        Append new observations to the dataset.
        """
        # if dataset contains no data yet
        if self.prev_states is None:
            self.__init__(sars_data)
        # append otherwise
        else:
            self.prev_states = np.concatenate((self.prev_states, self._dict_to_nparray(sars_data, 'prev_state')), axis=0)
            self.actions = np.concatenate((self.actions, self._dict_to_nparray(sars_data, 'action')), axis=0)
            self.rewards = np.concatenate((self.rewards, self._dict_to_nparray(sars_data, 'reward')), axis=0)
            self.new_states = np.concatenate((self.new_states, self._dict_to_nparray(sars_data, 'new_state')), axis=0)


def main():
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    import environments.lqr
    batch_data = environments.lqr.main()

    sars_dataset = SARSDataset(batch_data)

    print(sars_dataset[0])
    print(sars_dataset[0:3])
    return sars_dataset

if __name__ == '__main__':
    main()