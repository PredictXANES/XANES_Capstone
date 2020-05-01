import numpy as np
import pandas as pd
import random


def xanes_average(bootstraps, path, n):
    '''
    This function bootstraps through random samples of XANES Spectra to calculate the weighted average of the
    coordination number and absorption intensities. It outputs three dataframes, the first contains the coordination
    numbers and absorption intensities, the second contains the systems averaged for each new spectra, and the third
    contains the weights used for each system to compute the average.
    Inputs:
        bootstraps = The number of samples to take/averages to calculate. i.e. 10,000.
        path = Path of "XANES_ML_Data.xlsx" file
        n = Maximum number of spectra to average for each sampling. Function will choose between 2 and n spectra to
        average.
    '''
    data = pd.read_excel(path)

    mu_labels = []
    system_labels = []
    weight_labels = []

    for j in range(n + 1):
        if j == 0:
            pass
        else:
            system_labels.append("System" + str(j))
            weight_labels.append("Weight" + str(j))

    for nums in range(101):
        if nums == 0:
            pass
        else:
            mu_labels.append("Mu" + str(nums))

    averages_mu = []
    averages_systems = []
    averages_weights = []
    averages_cn = []
    for i in range(bootstraps):
        rand_num = random.randint(2, n)
        sample = data.sample(n=rand_num)
        weights = np.random.dirichlet(np.ones(rand_num), 1)
        weights = pd.Series(np.reshape(weights, -1))
        systems = sample[['System']]
        energies = sample[mu_labels]
        cn = sample['CN']
        weighted_cn = cn.mul(weights.values, axis=0)
        weighted_cn = weighted_cn.sum(axis=0)
        weighted_mu = energies.mul(weights.values, axis=0)
        weighted_mu = weighted_mu.sum(axis=0)
        averages_mu.append(np.asarray(weighted_mu))
        averages_systems.append(np.reshape(np.asarray(systems), -1))
        averages_weights.append(np.asarray(weights))
        averages_cn.append(weighted_cn)

    cn_averaged = pd.DataFrame(averages_cn, columns=['CN'])
    mu_averaged = pd.DataFrame(averages_mu, columns=mu_labels)
    mu_cn_averaged = pd.concat([cn_averaged, mu_averaged], axis=1)
    systems_averaged = pd.DataFrame(averages_systems, columns=system_labels)
    weights_averaged = pd.DataFrame(averages_weights, columns=weight_labels)

    return mu_cn_averaged, systems_averaged, weights_averaged