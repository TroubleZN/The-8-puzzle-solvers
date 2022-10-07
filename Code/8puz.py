#%%
import os
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

        state = states.pop(0)
        path = paths.pop(0)
        closed.add(str(state))
        nums += 1

        for direction in ["R", "L", "U", "D"]:
            state_new, path_new = move(state, path, direction)
            if state_new and str(state_new) not in closed:
                if state_new == [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "_"]]:
                    return nums, time.time()-start_time, path_new

                paths.append(path_new)
                states.append(state_new)


#%% DEPTH-LIMITED-SEARCH
def dls(state0, depth):
    start_time = time.time()
    frontier = [state0]
    paths = [""]
    closed = set()
    closed_info = {}
    nums = 0
    while len(frontier) > 0:
        state = frontier.pop()
        path = paths.pop()
        closed.add(str(state))
        closed_info[str(state)] = path
        nums += 1
        if len(path) == depth:
            cutoff = True
        else:
            for direction in ["R", "L", "U", "D"]:
                state_new, path_new = move(state, path, direction)
                if state_new:
                    if state_new == [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "_"]]:
                        return time.time() - start_time, nums, path_new
                    if str(state_new) not in closed:
                        paths.append(path_new)
                        frontier.append(state_new)
                    if str(state_new) in closed and len(path_new) < len(closed_info[str(state_new)]):
                        paths.append(path_new)
                        frontier.append(state_new)
                        closed_info[str(state_new)] = path_new
    return "cutoff", nums


#%% ITERATIVE-DEEPENING-SEARCH
def ids(state0):
    start_time = time.time()
    depth = 0
    nums = 0
    while 1:
        if time.time()-start_time >= 60*15:
            print("Total nodes generated: <<??>>")
            print("Total time taken: >15 min")
            print("Path length: Timed out.")
            print("Path: Timed out.")
            return False

        res = dls(state0, depth)
        nums += res[1]
        if res[0] != "cutoff":
            return nums, time.time() - start_time, res[2]
        depth += 1


#%% misplaced title heuristic. (h1)
def h1(state):
    n = 0
    index = 1
    for i in range(3):
        for j in range(3):
            if state[i][j] != str(index) and i+j != 4:
                n += 1
            index += 1
    return n


#%% Manhattan distance heuristic. (h2)
def h2(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != "_":
                num = int(state[i][j]) - 1
                row = num // 3
                col = num % 3
                distance += abs(row - i) + abs(col - j)
    return distance


#%% My heuristic. (h3)

# def h3(state):
#     n = 0
#     index = 1
#     if state[2][2] == "_":
#         n = 1
#     for i in range(3):
#         for j in range(3):
#             if state[i][j] != str(index) and i+j != 4:
#                 n += 1
#             index += 1
#     return n

def h3(state):
    state_temp = copy.deepcopy(state)
    n = 0
    while state_temp != [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "_"]]:
        blank_position = [(i, row.index("_")) for i, row in enumerate(state_temp) if "_" in row][0]
        if blank_position == (2, 2):
            for i in range(3):
                for j in range(3):
                    if state_temp[i][j] != str(3*i + j + 1):
                        state_temp[2][2] = state_temp[i][j]
                        state_temp[i][j] = "_"
                        break
                if state_temp[i][j] == "_":
                    break
        else:
            true_num = 3*blank_position[0] + blank_position[1] + 1
            num_position = [(i, row.index(str(true_num))) for i, row in enumerate(state_temp) if str(true_num) in row][0]
            state_temp[num_position[0]][num_position[1]] = "_"
            state_temp[blank_position[0]][blank_position[1]] = str(true_num)
        n += 1
    return n



# def h3(state):
#     distance = 0
#     for i in range(3):
#         for j in range(3):
#             if state[i][j] != "_":
#                 num = int(state[i][j]) - 1
#                 row = num // 3
#                 col = num % 3
#                 distance += (abs(row - i) + abs(col - j)) * (4-row-col)
#     return distance


#%% A* search
def H(state, h):
    if h == 1:
        return h1(state)
    elif h == 2:
        return h2(state)
    else:
        return h3(state)


def A_star(state0, h):
    start_time = time.time()
    closed = set()
    closed_info = {}
    paths = [""]
    states = [state0]
    Fs = [H(state0, h)]
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

        zipped = sorted(zip(Fs, paths, states))
        Fs, paths, states = zip(*zipped)
        Fs, paths, states = list(Fs), list(paths), list(states)

        state = states.pop(0)
        path = paths.pop(0)
        F = Fs.pop(0)
        closed.add(str(state))
        closed_info[str(state)] = [path, F]
        nums += 1

        for direction in ["R", "L", "U", "D"]:
            state_new, path_new = move(state, path, direction)
            if state_new:
                if state_new == [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "_"]]:
                    return nums + len(states), time.time() - start_time, path_new
                F_new = H(state_new, h) + len(path_new)
                if str(state_new) not in closed:
                    paths.append(path_new)
                    states.append(state_new)
                    Fs.append(F_new)
                if str(state_new) in closed and len(path_new) < len(closed_info[str(state_new)][0]):
                    paths.append(path_new)
                    states.append(state_new)
                    Fs.append(F_new)
                    closed_info[str(state_new)] = [path_new, F_new]




#%% check the solvability of the problem
def check_solvability(state0):
    state0_f = [s for a in state0 for s in a]
    n_inv = 0
    for i in range(9):
        for j in range(i+1, 9):
            if state0_f[i] != "_" and state0_f[j] != "_":
                if int(state0_f[i]) > int(state0_f[j]):
                    n_inv += 1
    # print(n_inv)
    if n_inv % 2:
        return False
    else:
        return True


#%% main body of solver function
def solver(fPath, alg, print_enable=True):
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
        res = A_star(state0, 1)
    elif alg == "h2":
        res = A_star(state0, 2)
    elif alg == "h3":
        res = A_star(state0, 3)
    else:
        print("Algorithm is not valid!")

    if print_enable:
        print("Total nodes generated:", res[0])
        if res[1] > 0.1:
            print("Total time taken:", round(res[1], 2), "sec")
        else:
            print("Total time taken:", round(1000*res[1], 2), "ms")
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

    # # Part 2
    # if len(pars) <= 1:
    #
    #     data_path = "../Data/Part2/"
    #     files = os.listdir(data_path)
    #     for file in files:
    #         for method in ["BFS", "IDS", "h1", "h2", "h3"]:
    #             print(color.BOLD + '\nData used is:\t' + data_path + file + color.END)
    #             print(color.BOLD + 'Method used is:\t' + method + color.END)
    #             solver(data_path + file, method)

    # Part 3
    if len(pars) <= 1:
        data_path = "../Data/Part3/"
        levels = os.listdir(data_path)
        for level in levels:
            print(color.RED + '\nLevel is:\t' + level + color.END)
            files = os.listdir(data_path + level)
            for method in ["h3"]:

                node_all = []
                time_all = []
                for file in files:
                    file_path = data_path + level + "/" + file
                    nums_node, time_used, path = solver(file_path, method, False)
                    node_all.append(nums_node)
                    time_all.append(time_used)
                print(color.RED + '\nMethod used is:\t' + method + color.END)
                print(color.RED + "Average time used:\t", str(sum(time_all)/len(time_all)), color.END)
                print(color.RED + "Average nodes explored:\t", sum(node_all)/len(node_all), color.END)






