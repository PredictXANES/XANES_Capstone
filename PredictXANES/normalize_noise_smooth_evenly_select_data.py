import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline

def normalization_spectra(df):
    '''
    use a raw spectra as parameter and return the after normalization spectra(np.array)
    all of the data are dividede by the highest absorption
    '''
    features=np.array(df.loc[:,'Mu1':'Mu100'])
    normalization_features = np.array([[0.0]*(np.size(features, 1))]*(np.size(features, 0)))
    for i in range(len(features)):
        max_absorption = np.amax(features[i])
        j = 0
        for absorption in features[i]:
            normlization_absoprtion = absorption/max_absorption
            normalization_features[i][j]=normlization_absoprtion
            j=j+1
    return normalization_features

def add_noise_to_averaged_spectra_df_return_smooth(df, std=0.015, windowSize=51, polynomial=2):
    '''
    pre: df should have columns named "Mu1" to "Mu100"
    add noise to the spectra, e.g default: np.random.normal(0,0.015,1000)
    post:return the np.array, each spectra after smooth mu value; 
    '''
    if 'Mu1' in df.columns:
        features=np.array(df.loc[:,'Mu1':'Mu100'])
    else:
        features=np.array(df)
            
    xs = np.linspace(8970, 9050, 1000)
    energies = np.linspace(8970, 9050, 100)
    smooth=np.array([])
    for i in range(features.shape[0]):
        s1 = UnivariateSpline(energies, features[i], s=0)
        y1 = s1(xs) # generate a line with 1000 data, the amount of data depend on the xs num the third parameter
        noise = np.random.normal(0,std,1000)
        y2 = y1+ noise
        ysmooth = savgol_filter(y2, windowSize, polynomial)
        smooth = np.concatenate((smooth,ysmooth),axis=0)
        
    # return the smooth spectra np.array
    after_smooth=smooth.reshape(len(df.index),1000)
    return after_smooth

def add_noise(df,std=0.015):
    if 'Mu1' in df.columns:
        features=np.array(df.loc[:,'Mu1':'Mu100'])
    else:
        features=np.array(df)
            
    xs = np.linspace(8970, 9050, 1000)
    energies = np.linspace(8970, 9050, 100)
    y_noise=np.array([])
    for i in range(features.shape[0]):
        s1 = UnivariateSpline(energies, features[i], s=0)
        y1 = s1(xs) # generate a line with 1000 data, the amount of data depend on the xs num the third parameter
        noise = np.random.normal(0,std,1000)
        y2 = y1+ noise
        y_noise = np.concatenate((y_noise,y2),axis=0)
    return y_noise.reshape(len(df.index),1000)

def smooth_spectra(ndarray,windowSize=51, polynomial=2):
    smooth=np.array([])
    for i in range(len(ndarray)):
        y2 = ndarray[i]
        ysmooth = savgol_filter(y2, windowSize, polynomial)
        smooth = np.concatenate((smooth,ysmooth),axis=0)
    after_smooth=smooth.reshape(len(ndarray),len(ndarray[0]))
    return after_smooth

def one_demension_get_N_evenly_spaced_elements(arr, numElems):
    '''
    paramter: arr: one row(one spetrum)
    numElems: type int, how many data points to be selected in a spectrum
    return nd.array
    '''
    idx = np.round(np.linspace(0, len(arr) - 1, numElems)).astype(int)
    return arr[idx]
    
def ndArray_get_N_evely_spaced_elements(after_smooth, numElems):
    '''
    take a nd.array as paramter, e.g. each row is the smoothed line with 1000 data point
    numElems type int, how many data points to be selected in a spectrum, e.g. 100 data points from 1000 data points
    for each spectrum(row)
    return the nd.array which only contain the selected points for every spectra(row)
    '''
    ndArray_evenly_spaced=np.array([])
    for arr in after_smooth:
        a_row_evenly_spaced=one_demension_get_N_evenly_spaced_elements(arr, numElems)
        print(a_row_evenly_spaced)
        ndArray_evenly_spaced  = np.append(ndArray_evenly_spaced, a_row_evenly_spaced, axis=0)
    return ndArray_evenly_spaced.reshape(len(after_smooth),numElems)

