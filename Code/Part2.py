
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

import os
from ./Code/8puz import *


if len(pars) <= 1:

    data_path = "../Data/Part2/"
    files = os.listdir(data_path)
    for file in files:
        for method in ["BFS", "IDS", "h1", "h2", "h3"]:
            print(color.BOLD + '\nData used is:\t' + data_path + file + color.END)
            print(color.BOLD + 'Method used is:\t' + method + color.END)
            solver(data_path + file, method)