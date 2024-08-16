import pandas as pd
import scipy.io as spio
import numpy as np
import scipy
from scipy.interpolate import InterpolatedUnivariateSpline

def __loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    def _check_keys(d):
        '''
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        '''
        for key in d:
            if isinstance(d[key], scipy.io.matlab.mat_struct):
                d[key] = _todict(d[key])
        return d

    def _todict(matobj):
        '''
        A recursive function which constructs from matobjects nested dictionaries
        '''
        d = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, scipy.io.matlab.mat_struct):
                d[strg] = _todict(elem)
            elif isinstance(elem, np.ndarray):
                d[strg] = _tolist(elem)
            else:
                d[strg] = elem
        return d

    def _tolist(ndarray):
        '''
        A recursive function which constructs lists from cellarrays
        (which are loaded as numpy ndarrays), recursing into the elements
        if they contain matobjects.
        '''
        elem_list = []
        for sub_elem in ndarray:
            if isinstance(sub_elem, scipy.io.matlab.mat_struct):
                elem_list.append(_todict(sub_elem))
            elif isinstance(sub_elem, np.ndarray):
                elem_list.append(_tolist(sub_elem))
            else:
                elem_list.append(sub_elem)
        return elem_list
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)


# include acceleration and impulse
def velocity_to_acceleration(timesteps, velocity):

  sp = InterpolatedUnivariateSpline(timesteps,velocity)
  return sp.derivative()(timesteps)


def loadMatlab(filename) -> tuple[list, list]:
    '''
    Overview:
    ------------
    The `loadMatlab` function is designed to load and process MATLAB `.mat` files containing neural and kinematic data, organized under the `kinAggrogate` structure. It converts the MATLAB data into a format suitable for further analysis in Python, separating neural activity data and continuous kinematic data.

    Parameters:
    ------------
    - filename: str
        The path to the MATLAB `.mat` file to be loaded. This file should contain the `kinAggrogate` structure with neural and kinematic data.

    Returns:
    ------------
    - neural_stim: list of lists
        A list containing neural activity data for each stimulation session. Each element in the list is a sublist representing a session, and the sublist contains arrays of neural data matrices.
    
    - continous_stim: list of lists
        A list containing continuous kinematic data for each stimulation session. Each element in the list is a sublist representing a session, and the sublist contains arrays of kinematic data matrices. The kinematic data also includes additional acceleration data derived from velocity components.
    '''


    # load matlab
    b = __loadmat(filename)
    
    # convert matlab
    neural_stim = []
    continous_stim = []

    for i in b['kinAggrogate'].keys():

        stim = b['kinAggrogate'][i]

        neural_session = []
        continous_sessions = []

        for k in stim.keys():
            print(f"\t Organizing {k}")
            dataMatrix = np.array(stim[k])

            if k[0] == "n":

                neural_session += [dataMatrix[:,1:]]

            if k[0] == "l" and k[1] != "a":

                x = velocity_to_acceleration(dataMatrix[:,0], dataMatrix[:,-3]).reshape(-1,1)
                y = velocity_to_acceleration(dataMatrix[:,0], dataMatrix[:,-2]).reshape(-1,1)
                z = velocity_to_acceleration(dataMatrix[:,0], dataMatrix[:,-1]).reshape(-1,1)

                print(dataMatrix.shape, x.shape)

                dataMatrix = np.hstack([dataMatrix, x, y, z])

                continous_sessions += [dataMatrix[:,1:]]

        neural_stim += [neural_session]
        continous_stim += [continous_sessions]
    
    return neural_stim, continous_stim

