#%%
import time
import copy
import numpy as np


#%% Moves
def move(state, path, direction):
    state = copy.deepcopy(state)

    dims = state.__len__()
    blank_position = [(i, row.index("_")) for i, row in enumerate(state) if "_" in row][0]

    if direction == "R":
        if blank_position[1] == 0:
            # print("WARNING: The move is illegal! The move is canceled.")
            return 0, 0
        else:
            state[blank_position[0]][blank_position[1]] = state[blank_position[0]][blank_position[1] - 1]
            state[blank_position[0]][blank_position[1] - 1] = "_"
            path += direction

    elif direction == "L":
        if blank_position[1] == dims-1:
            # print("WARNING: The move is illegal! The move is canceled.")
            return 0, 0
        else:
            state[blank_position[0]][blank_position[1]] = state[blank_position[0]][blank_position[1] + 1]
            state[blank_position[0]][blank_position[1] + 1] = "_"
            path += direction

    elif direction == "U":
        if blank_position[0] == dims-1:
            # print("WARNING: The move is illegal! The move is canceled.")
            return 0, 0
        else:
            state[blank_position[0]][blank_position[1]] = state[blank_position[0] + 1][blank_position[1]]
            state[blank_position[0] + 1][blank_position[1]] = "_"
            path += direction

    elif direction == "D":
        if blank_position[0] == 0:
            # print("WARNING: The move is illegal! The move is canceled.")
            return 0, 0
        else:
            state[blank_position[0]][blank_position[1]] = state[blank_position[0] - 1][blank_position[1]]
            state[blank_position[0] - 1][blank_position[1]] = "_"
            path += direction

    else:
        # print("WARNING: The move is illegal! The move is canceled.")
        return 0, 0

    return state, path


#%% BFS
def bfs(state0):
    start_time = time.time()
    closed = set()
    paths = [""]
    states = [state0]
    nums = 0
    while 1:
        if time.time()-start_time >= 60*15:
            return False

        if not states:
            return False

        state = states.pop(0)
        path = paths.pop(0)
        closed.add(str(state))

        for direction in ["R", "L", "U", "D"]:
            state_new, path_new = move(state, path, direction)
            if state_new and str(state_new) not in closed:
                if state_new == [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "_"]]:
                    return len(closed), time.time()-start_time, path_new

                nums += 1
                paths.append(path_new)
                states.append(state_new)


#%% main body of solver function
def solver(data_path, method):
    # load data
    state0 = np.loadtxt(data_path, "str").tolist()

    # find solution
    if method == "BFS":
        res = bfs(state0)
    elif method == "IDS":
        res = ids(state0)
    elif method == "h1":
        res = h1(state0)
    elif method == "h2":
        res = h2(state0)
    elif method == "h3":
        res = h3(state0)

    print("Total nodes generated:", res[0])
    print("Total time taken:", round(res[1], 2), "sec")
    print("Path length:", len(res[2]))
    print("Path:", res[2])
    return res


#%%
if __name__ == '__main__':
    # var = input()
    # print("You entered: " + var)
    import sys

    if len(sys.argv) == 3:
        data_path = sys.argv[1]
        method = sys.argv[2]
        print("The data used is:\t", data_path)
        print("The method used is:\t", method, "\n")
        res = solver(data_path, method)
    else:
        print("\nPlease provide the path for the data and the method desired. \n")
        data_path = "../Data/Part2/S1.txt"
        method = "BFS"
        print("The data used is:\t", data_path)
        print("The method used is:\t", method, "\n")
        res = solver(data_path, method)