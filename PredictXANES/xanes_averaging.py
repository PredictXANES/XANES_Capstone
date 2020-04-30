import pandas as pd
import random

data = pd.read_excel('XANES_ML_Data.xlsx')
bootstraps = 1000

mu_labels = []
for nums in range(101):
    if nums == 0:
        pass
    else:
        mu_labels.append("Mu" + str(nums))

for i in range(bootstraps):
    rand_averages = random.randint(2, 10)
    n = []
    for j in range(rand_averages):
        rand_idx = random.randint(0, len(data)-1)
        n.append(rand_idx)
    rand_data = data.iloc[n]
    labels = rand_data[['System', 'Central_atom']]
    energies = rand_data[mu_labels]
    energies = pd.DataFrame(energies.mean(axis=0))
    energies = energies.transpose()
    df = pd.concat([labels, energies],axis=1)
    print(df)