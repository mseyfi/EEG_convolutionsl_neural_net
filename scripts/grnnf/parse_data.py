import random, data_manip

import numpy as np

from scipy.io import loadmat

from keras.utils import np_utils

def parse_data(data_path):
    
    trial_number = 0
    trials = []
    labels = []
    for i in range(1,11):
        subject = loadmat(data_path + "S" + str(i) + ".mat")
        trial_number = trial_number + subject["T"][0][0]
        electrodes = 124
        timesteps = subject["N"][0][0]
        trials.extend(subject["X_2D"])
        labels.extend(subject["exemplarLabels"][0])

    X_train = []
    Y_train = []

    X_test = []
    Y_test = []

    data = list(zip(trials, labels))

    random.shuffle(data)

    trials, labels = zip(*data)

    for i in range(0, trial_number - 500):
        X_train.append(np.reshape(trials[i], (electrodes, timesteps)))
        Y_train.append(labels[i]-1)

    for i in range(trial_number-5000, trial_number):
        X_test.append(np.reshape(trials[i], (electrodes, timesteps)))
        Y_test.append(labels[i]-1)

    X_train = np.array(X_train)
    X_train = X_train.reshape(X_train.shape[0], 1, 124, 32)

    X_test = np.array(X_test)
    X_test = X_test.reshape(X_test.shape[0], 1, 124, 32)

    Y_train = np.array(Y_train)
    Y_test = np.array(Y_test)

    Y_train = np_utils.to_categorical(Y_train, 72)
    Y_test = np_utils.to_categorical(Y_test, 72)
    
    data_dict = {"X_train": X_train, "Y_train": Y_train, "X_test": X_test, "Y_test": Y_test}
    data_manip.save_data("../../preprocessed_data/ppd_exemplar.json", data_dict)
    return data_dict
