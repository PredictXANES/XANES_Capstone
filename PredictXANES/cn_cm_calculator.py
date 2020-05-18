import os
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
from check_central_atom import central_atoms

def cn_cm_calculator(rootdir, k, r):
    '''
    This function calculates and returns the coordination number and coulomb matrix for a central atom in a set of CuTe
    systems used to simulate XANES spectra.
    Inputs:
        rootdir = Root directory of folder containing the structural information "feff.inp" file for the systems.
        An example for this is: "C:/Users/justi/Desktop/DIRECT Capstone XANES ML/Folders_with_XANES_and_structures"
        k = The number of nearest neighbors used to calculate the coulomb matrix for the central atom. The self term
        is neglected, so k = 21 will calculate the coulomb matrix for the 20 nearest atoms to the central atom.
        r = The radius cutoff for determining the nearest neighbors to count for the coordination number.

    Outputs:
        df1 = Dataframe that contains the Central Atom label and the Coulomb Matrix for the k neareast neighbors.
        df2 = Dataframe that contains the Central Atom label, the coordination number, number of copper atoms, and
        the number of tellurium atoms within r radius of the central atom.
    '''

    # Import list of the central copper atoms
    atoms_df = central_atoms(rootdir)

    i = 0  # Manual counter for central atom list

    overall_cm = []
    overall_cn = []
    overall_num_cu = []
    overall_num_te = []

    # Walk through root directory for the structure_data.csv for each system
    for subdir, dir, files in os.walk(rootdir):
        for file in files:
            if file == 'structure_data.csv':
                central_cu = atoms_df['Central_atom'].iloc[i]

                data = pd.read_csv(os.path.join(subdir, file))  # Imports each system as a dataframe

                # Structure data for Neareast Neighbors fitting
                X = np.empty([len(data), 3])
                X[:, 0] = data['x']
                X[:, 1] = data['y']
                X[:, 2] = data['z']

                idx = data.loc[data['label'] == central_cu].index[0]  # Index value for the central atom
                tree = KDTree(X, metric='euclidean')  # Train tree from x,y,z data and calculate euclidean distance
                distances, indices = tree.query(X, k=k)  # Tree to calculate euclidean distance for 21 nearest neighbors

                cu0_distances = distances[idx, :]  # Distances for neighbors nearest to central copper
                cu0_indices = indices[idx, :]  # Indices for neighbors nearest to central copper
                cu0_atoms = np.array(data.loc[cu0_indices, 'atom'])  # Atom labels (0, 1, 2 ,3) for nearest neighbors

                atom_dict = {0: 29, 1: 29, 2: 29, 3: 52}  # Dictionary matching atom label with atomic number Z

                # query tree for # of nearest neighbors within 3 A.
                cn_tree = tree.query_radius(X, r=r, count_only=True)
                ind = tree.query_radius(X, r=r)
                ind = list(ind[idx])
                ind.remove(idx)
                cn_df = data.loc[ind]
                num_cu1 = (cn_df.atom == 1.0).sum()
                num_cu2 = (cn_df.atom == 2.0).sum()
                num_cu = num_cu1 + num_cu2
                num_te = (cn_df.atom == 3.0).sum()
                cn = cn_tree[idx] - 1  # subtract self as a nearest neighbors for coordination number

                cm = []  # Coulomb matrix
                for j in range(len(cu0_atoms)):
                    if j >= 1:
                        cm.append(atom_dict[cu0_atoms[0]] * atom_dict[cu0_atoms[j]] / cu0_distances[j])
                    else:
                        pass

                overall_cm.append(cm)
                overall_cn.append(cn)
                overall_num_cu.append(num_cu)
                overall_num_te.append(num_te)

                i += 1
            else:
                pass
    cm_df = pd.DataFrame(overall_cm)
    cu_df = pd.DataFrame(overall_num_cu, columns=['Num Cu'])
    te_df = pd.DataFrame(overall_num_te, columns=['Num Te'])
    cn_df = pd.DataFrame(overall_cn, columns=['Coordination Number'])
    df1 = pd.concat([atoms_df, cm_df], axis=1, sort=False)
    df2 = pd.concat([atoms_df, cn_df, cu_df, te_df], axis=1, sort=False)

    return df1, df2
