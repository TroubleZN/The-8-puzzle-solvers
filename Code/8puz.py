#%% load packages
import numpy as np


#%% main body of solver function
def solver(data_path, method):
    # load data
    state0 = np.loadtxt(data_path, "str").tolist()

    # find solution


