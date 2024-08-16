from src.cebraAnalysis import model
from src.matlab_util import loadMatlab
from sklearn.model_selection import train_test_split
import numpy as np


matlabFile = ""

def main():
    
    # load neuralpixel data in from compiled matlab file
    neural_stim, continous_stim = loadMatlab(matlabFile)

    # split stimulius 0 into a test/training set. %30 test, %70 training
    indices = np.arange(len(neural_stim[0]))
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(neural_stim[0], continous_stim[0], indices, test_size=0.3, random_state=42)

    # Columns: x, y, z, velocity, velocity_x, velocity_y,velocity_z, accelerationn_x, acceleration_y, acceleration_z
    y_train_x_only = [reach[:, :1] for reach in y_train]

    # intialize & train model
    stim_0 = model()
    stim_0.train(X_train, y_train_x_only)

    # examine output
    print(f"Train R^2: {np.asarray(stim_0.examine(X_train, y_train_x_only)).flatten().mean()}")
    print(f"Test R^2: {np.asarray(stim_0.examine(X_test, y_test)).flatten().mean()}")

    '''
    < Include your own analysis > 
    '''


if __name__ == "__main__":
    main()