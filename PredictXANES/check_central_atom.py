import pandas as pd
import os


def central_atoms(rootdir):
    '''
    This functions returns a dataframe that contains the labels of the central atom used in each system.
    Inputs:
        rootdir = Root directory of folder containing the structural information "feff.inp" file for the systems.
        An example for this is: "C:/Users/justi/Desktop/DIRECT Capstone XANES ML/Folders_with_XANES_and_structures"

    Outputs:
        df = Dataframe that contains the central atom labels.
    '''

    system_list = []
    cent_cu_list = []
    for subdir, dir, files in os.walk(rootdir):
        for file in files:
            if file == 'structure_data.csv':
                full_name = subdir
                sys = full_name.partition('\\')
                sys = sys[2]
                sys = sys.replace('-Cu', '/Cu')
                partitioned_name = full_name.partition('-Cu')
                cent_cu_label = (partitioned_name[1] + partitioned_name[2])[1:]
                cent_cu_list.append(cent_cu_label)
                system_list.append(sys)
            else:
                pass
    df1 = pd.DataFrame(system_list, columns=['System'])
    df2 = pd.DataFrame(cent_cu_list, columns=['Central_atom'])
    df = pd.concat([df1, df2], axis=1, sort=False)
    return df

df = central_atoms("C:/Users/justi/Desktop/DIRECT Capstone XANES ML/Folders_with_XANES_and_structures")
df.to_csv('central_copper_list.csv', index=False)