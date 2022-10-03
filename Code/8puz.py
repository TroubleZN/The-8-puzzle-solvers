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


#%% BREADTH-FIRST-SEARCH
def bfs(state0):
    start_time = time.time()
    closed = set()
    paths = [""]
    states = [state0]
    nums = 0
    while 1:
        if time.time()-start_time >= 60*15:
            print("Total nodes generated: <<??>>")
            print("Total time taken: >15 min")
            print("Path length: Timed out.")
            print("Path: Timed out.")
            return False

        if not states:
            return False

        state = states.pop()
        path = paths.pop()
        closed.add(str(state))
        nums += 1

        for direction in ["R", "L", "U", "D"]:
            state_new, path_new = move(state, path, direction)
            if state_new and str(state_new) not in closed:
                if state_new == [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "_"]]:
                    return len(closed), time.time()-start_time, path_new

                paths.append(path_new)
                states.append(state_new)


#%% DEPTH-LIMITED-SEARCH
def dls(state0, depth):
    start_time = time.time()
    frontier = [state0]
    paths = [""]
    cutoff = False
    closed = set()
    nums = 0
    while len(frontier) > 0:
        state = frontier.pop()
        path = paths.pop()
        closed.add(str(state))
        nums += 1
        if len(path) == depth:
            cutoff = True
        else:
            for direction in ["R", "L", "U", "D"]:
                state_new, path_new = move(state, path, direction)
                if state_new and str(state_new) not in closed:
                    if state_new == [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "_"]]:
                        return cutoff, nums, time.time() - start_time, path_new

                    paths.append(path_new)
                    frontier.append(state_new)
    return cutoff, nums


#%% ITERATIVE-DEEPENING-SEARCH
def ids(state0):
    depth = 0
    nums = 0
    while 1:
        res = dls(state0, depth)
        nums += res[1]
        print(depth,nums)
        if not res[0]:
            return nums, res[2:]
        depth += 5


#%% check the solvability of the problem
def check_solvability(state0):
    state0_f = [s for a in state0 for s in a]
    n_inv = 0
    for i in range(9):
        for j in range(i+1, 9):
            if state0_f[i] > state0_f[j]:
                n_inv += 1
    if n_inv % 2:
        return False
    else:
        return True


#%% main body of solver function
def solver(fPath, alg):
    # load data
    state0 = np.loadtxt(fPath, "str").tolist()

    # check solvability
    solvability = check_solvability(state0)
    if not solvability:
        print("The inputted puzzle is not solvable:")
        for a in state0:
            print(*a)
        return False

    # find solution
    res = [0, 0, ""]
    if alg == "BFS":
        res = bfs(state0)
    elif alg == "IDS":
        res = ids(state0)
    elif alg == "h1":
        res = h1(state0)
    elif alg == "h2":
        res = h2(state0)
    elif alg == "h3":
        res = h3(state0)
    else:
        print("Algorithm is not valid!")

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

    pars = sys.argv[1:]
    n_pars = len(pars)

    if "--fPath" not in pars or "--alg" not in pars or pars[0] == "-h" or len(pars) != 4:
        print("Please provide the path for the data and the method desired.")
        print("8puz.py --fPath file_path --alg algorithm")
        # data_path = "../Data/Part2/S1.txt"
        # method = "BFS"
        # print("The data used is:\t", data_path)
        # print("The method used is:\t", method, "\n")
        # res = solver(data_path, method)
    else:
        for i in range(n_pars):
            if pars[i] == "--fPath" and i+1 < n_pars:
                data_path = pars[i+1]
            if pars[i] == "--alg" and i+1 < n_pars:
                method = pars[i+1]
        print("The data used is:\t", data_path)
        print("The method used is:\t", method, "\n")
        res = solver(data_path, method)

    data_path = "../Data/Part2/S1.txt"
    state0 = np.loadtxt(data_path, "str").tolist()
    ids(state0)


