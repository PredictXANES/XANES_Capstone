import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree

data = pd.read_csv('C:/Users/justi/Desktop/DIRECT Capstone XANES ML/Folders_with_XANES_and_structures/'
                   'Cu1.5Te-629332-full-Cu1.0/structure_data.csv')
idx = data.loc[data['atom']==0].index[0]  # Central copper index value
data.drop(['Unnamed: 0'], axis=1, inplace=True)  # Deleting arbitrary column

X = np.empty([1254, 3])  # Generating x, y, z matrix for every atom
for i in range(1254):
    for j in range(3):
        X[i,j] = data.iloc[i, j]

tree = KDTree(X, metric='euclidean')
distances, indices = tree.query(X, k=13)  # Tree to calculate euclidean distance for 13 nearest neighbors

cu0_distances = distances[idx, :]  # Distances for neighbors nearest to central copper
cu0_indices = indices[idx, :]  # Indices for neighbors nearest to central copper
cu0_atoms = np.array(data.loc[cu0_indices, 'atom'])  # Atom labels (0, 1, 2 ,3) for neighbors nearest to central copper

atom_dict = {0: 29, 1: 29, 2: 29, 3: 52}  # Dictionary matching atom label with atomic number Z

cm = []  # Coulomb matrix
for j in range(len(cu0_atoms)):
    if j >= 1:
        cm.append(atom_dict[cu0_atoms[0]] * atom_dict[cu0_atoms[j]] / cu0_distances[j])
    else:
        pass
# Ignore j=0 because we don't need to compare central copper with itself

print(cm)