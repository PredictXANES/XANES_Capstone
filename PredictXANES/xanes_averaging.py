import numpy as np
import pandas as pd
import random
from cn_cm_calculator import cn_cm_calculator


def xanes_average(bootstraps, path, rootdir, n, r=3):
    '''
    This function bootstraps through random samples of XANES Spectra to calculate the weighted average of the
    coordination number and absorption intensities. It outputs three dataframes, the first contains the coordination
    numbers and absorption intensities, the second contains the systems averaged for each new spectra, and the third
    contains the weights used for each system to compute the average.
    Inputs:
        bootstraps = The number of samples to take/averages to calculate. i.e. 10,000.
        path = Path of "XANES_ML_Data.xlsx" file
        rootdir = Root directory of folder containing the structural information "feff.inp" file for the systems.
            An example for this is: "C:/Users/justi/Desktop/DIRECT Capstone XANES ML/Folders_with_XANES_and_structures"
        n = Maximum number of spectra to average for each sampling. Function will choose between 2 and n spectra to
            average.
        r = radius to calculate number of Cu and Te atoms nearest to central atom, defaulted to 3 for Cu-Te bond length.
    Outputs:
    mu_cn_averaged = Dataframe containing weighted average coordination number, number of Cu atoms within r distance,
        number of Te atoms within r distance, and averaged XANES absorption values for 100 energy points.
    systems_averaged = the n number of reference systems used to calculate the averaged spectra.
    weights_averaged = the weights used for each system, respectively, to calculated the averaged spectra.
    '''
    data = pd.read_excel(path)
    data = data.dropna(axis=1)
    df1, df2 = cn_cm_calculator(rootdir, r=r, k=21)
    df2 = df2.drop(['Central_atom', 'Coordination Number'], axis=1)
    data = pd.merge(data, df2, on='System')

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
    averages_cu = []
    averages_te = []
    for i in range(bootstraps):
        rand_num = random.randint(2, n)
        sample = data.sample(n=rand_num)
        weights = np.random.dirichlet(np.ones(rand_num), 1)
        weights = pd.Series(np.reshape(weights, -1))
        systems = sample[['System']]
        energies = sample[mu_labels]
        cn = sample['CN']
        num_cu = sample['Num Cu']
        num_te = sample['Num Te']
        weighted_cn = cn.mul(weights.values, axis=0)
        weighted_cn = weighted_cn.sum(axis=0)
        weighted_mu = energies.mul(weights.values, axis=0)
        weighted_mu = weighted_mu.sum(axis=0)
        weighted_num_cu = num_cu.mul(weights.values, axis=0)
        weighted_num_cu = weighted_num_cu.sum(axis=0)
        weighted_num_te = num_te.mul(weights.values, axis=0)
        weighted_num_te = weighted_num_te.sum(axis=0)
        averages_mu.append(np.asarray(weighted_mu))
        averages_systems.append(np.reshape(np.asarray(systems), -1))
        averages_weights.append(np.asarray(weights))
        averages_cn.append(weighted_cn)
        averages_cu.append(weighted_num_cu)
        averages_te.append(weighted_num_te)

    num_cu_averaged = pd.DataFrame(averages_cu, columns=['Num Cu'])
    num_te_averaged = pd.DataFrame(averages_te, columns=['Num Te'])
    cn_averaged = pd.DataFrame(averages_cn, columns=['CN'])
    mu_averaged = pd.DataFrame(averages_mu, columns=mu_labels)
    mu_cn_averaged = pd.concat([cn_averaged, num_cu_averaged, num_te_averaged, mu_averaged], axis=1)
    systems_averaged = pd.DataFrame(averages_systems, columns=system_labels)
    weights_averaged = pd.DataFrame(averages_weights, columns=weight_labels)

    return mu_cn_averaged, systems_averaged, weights_averaged

path = 'C:/Users/justi/Desktop/DIRECT Capstone XANES ML/XANES_ML_Data.xlsx'
# mu, sys, weights = xanes_average(100, path, 20)
# mu.to_csv("mu100.csv", index=False)
# sys.to_csv("sys100.csv", index=False)
# weights.to_csv("weights100.csv", index=False)
bootstraps = 10000
n = 20
rootdir = "C:/Users/justi/Desktop/DIRECT Capstone XANES ML/Folders_with_XANES_and_structures"

mu, sys, weights = xanes_average(bootstraps, path, rootdir, n, r=3)
mu.to_csv('mu_cn10000.csv', index=False)