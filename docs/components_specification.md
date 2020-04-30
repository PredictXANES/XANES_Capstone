Components:

1. data processing functions: 

1.a csv_to_df:

Inputs: multiple csv files each containing XANES spectrum and data labels, or one csv file of raw XANES data
Outputs: a list of lists that contain the spectra and labels, or one list which contains a spectrum

Given a XANES spectrum or set of spectra, along with labels for computer generated spectra, process this data 
into a list of sets of specrtum with labels. The labels include coordination number, central atom, and coulomb matrix.

1.b weighted_averaged_specrta:

Input: a list of lists that contain the spectra and labels
Output: a list of lists that contain averaged spectra along with labels

Given a list of XANES spectra, generate an averaged set of data along with the labels. 
The labels include averaged coordination number, weights and refference spectra.

2. Curve fitting functions:

2.a fit_full_spectrum
Inputs: a list of lists that contain the spectra and labels, or one list which contains a spectrum
Outputs: a list lists that contains the curves and labels, or one list that contains one curve 

Given the list of processed data, fit each spectrum into a model, and append the model to the set of lists

2.b fit_peaks:
Inputs: a list of lists that contain the spectra and labels, or one list which contains a spectrum
Outputs: a list lists that contains the peak curves and labels, or one list that contains one curve for each peak

Given a list of processed data, fit individual gaussian peaks to the spectra.

3. prediction functions:

3.a predict_coordination_number:

Inputs: a list of lists that contains the curves and labels, or one list that contains one curve
Output: coordination number of the compound

With fitted data, predict the coordination number of the compund that generated the data.

3.b predict_weights:

Inputs: a list of lists that contains the curves and labels, or one list that contains one curve
Output: weights of refference curves that generate the averaged spectrum

3.c predict_fewest_datapoints:

Inputs: a list of lists that contains the curves and labels, or one list that contains one curve
Output: coordination number, fewest datapoints needed to accurately fit a spectrum

With fitted data, predict the fewest datapoints needed to fit the spectrum accurately.