import pandas as pd
import numpy as np
from sklearn.metrics import auc


def spectrum_area(mu_df):
    '''
    This function calculates the area under a XANES spectrum for a series of averaged spectra.
    Inputs:
        mu_df = Pandas dataframe of averaged XANES spectra absorption values.
    Outputs:
        area = Pandas dataframe of area under the curve for averaged XANES spectra.
    '''

    energy = np.linspace(8970, 9050, 100)
    if 'CN' in mu_df.columns:
        mu_df = mu_df.drop(labels='CN', axis=1)
    else:
        pass
    mu_df = np.asarray(mu_df)
    area = []
    for i, item in enumerate(mu_df):
        area.append(auc(energy, mu_df[i,:]))
    area = pd.DataFrame(area, columns=['Area'])
    return area
