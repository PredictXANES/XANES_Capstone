Components:

1. data processing functions: 

Inputs: multiple csv files each containing XANES spectrum and data labels, or one csv file of raw XANES data
Outputs: a list of lists that contain the spectra and labels, or one list which contains a spectrum

Given a XANES spectrum or set of spectra, along with labels for computer generated spectra, process this data into a list of sets of specrtum with labels

2. Curve fitting function:

Inputs: a list of lists that contain the spectra and labels, or one list which contains a spectrum
Outputs: a list lists that contains the curves and labels, or one list that contains one curve 

Given the list of processed data, fit each spectrum into a model, and append the model to the set of lists

3. prediction functions:

3.a predict_coordination_number:

Inputs: a list lists that contains the curves and labels, or one list that contains one curve
Output: coordination number of the compound

With fitted data, predict the coordination number of the compund that generated the data.


3.b predict_fewest_datapoints:

Inputs: a list lists that contains the curves and labels, or one list that contains one curve
Output: coordination number, fewest datapoints needed to accurately fit a spectrum

With fitted data, predict the fewest datapoints needed to fit the spectrum accurately.