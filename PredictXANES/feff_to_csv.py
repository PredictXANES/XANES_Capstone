import pandas as pd
import numpy as np
import os


rootdir = 'C:/Users/justi/Desktop/DIRECT Capstone XANES ML/Folders_with_XANES_and_structures'
list1 = list(np.linspace(0, 36, 37))

for subdir, dir, files in os.walk(rootdir):
    for file in files:
        if file == 'feff.inp':
            data = pd.read_csv(os.path.join(subdir, file), skiprows=list1, nrows=1254, header=None, delimiter='\s+', names=['x', 'y', 'z', 'atom', 'label', 'bond_length'])
            data.to_csv(subdir+'\structure_data.csv')
        else:
            pass