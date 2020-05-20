import numpy as np

def xanes_derivatives(mu_df, dx=0.80808080808):
    '''
    This function calculates and returns the first and second derivative of a series of XANES spectra.
    Inputs:
        mu_df = Pandas dataframe of averaged XANES spectra absorption values.
        dx = distance between uniformly distributed energy values in XANES spectra. Defaulted to value provided in data.
    '''
    mu_labels = []
    for nums in range(101):
        if nums == 0:
            pass
        else:
            mu_labels.append("Mu" + str(nums))

    mu_df = mu_df[mu_labels]

    dmu1 = np.zeros([len(mu_df), len(mu_df.columns)-1])
    dmu2 = np.zeros([len(mu_df), np.shape(dmu1)[1]-1])

    for i in range(len(mu_df)):
        for j in range(np.shape(dmu1)[1]):
            dmu1[i, j] = (mu_df.iloc[i, j+1] - mu_df.iloc[i, j]) / dx

    for i_ in range(len(mu_df)):
        for j_ in range(np.shape(dmu2)[1]):
            dmu2[i_, j_] = (dmu1[i_, j_+1] - dmu1[i_, j_]) / dx

    return dmu1, dmu2