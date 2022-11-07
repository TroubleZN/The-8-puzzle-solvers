# The-8-puzzle-solvers
Five solvers are implemented using Python. 

File structure:\\
./\\
./Data/\\
./Data/Part2/\\
./Data/Part3/\\
./8puz.py\\
./README.txt\\

The solver can be called directly with:

python ./8puz.py --fPath file_path --alg algorithm

To automatically reproduce the results for Part 2 and 3:

python ./8puz.py --Part2

python ./8puz.py --Part3

## 1. BREADTH-FIRST-SEARCH

__function__ BREADTH-FIRST-SEARCH(_problem_) __returns__ a solution, or failure  
&emsp;__if__ problem's initial state is a goal __then return__ empty path to initial state  
&emsp;_frontier_ &larr; a FIFO queue initially containing one path, for the _problem_'s initial state  
&emsp;_reached_ &larr; a set of states; initially empty  
&emsp;_solution_ &larr; failure  
&emsp;__while__  _frontier_ is not empty __do__  
&emsp;&emsp;&emsp;_parent_ &larr; the first node in _frontier_  
&emsp;&emsp;&emsp;__for__ _child_ __in__ successors(_parent_) __do__   
&emsp;&emsp;&emsp;&emsp;&emsp;_s_ &larr; _child_.state  
&emsp;&emsp;&emsp;&emsp;&emsp;__if__ _s_ is a goal  __then__  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;__return__  _child_  
&emsp;&emsp;&emsp;&emsp;&emsp;__if__ _s_ is not in _reached_ __then__  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;add _s_ to _reached_  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;add _child_ to the end of _frontier_  
&emsp;__return__  _solution_


## 2. DEPTH-LIMITED-SEARCH

__function__ DEPTH-LIMITED-SEARCH(_problem_, _l_) __returns__ a solution, or failure, or cutoff  
&emsp;_frontier_ &larr; a FIFO queue initially containing one path, for the _problem_'s initial state  
&emsp;_solution_ &larr; failure  
&emsp;__while__  _frontier_ is not empty __do__  
&emsp;&emsp;&emsp;_parent_ &larr; pop(_frontier_)  
&emsp;&emsp;&emsp;__if__ depth(_parent_) > l __then__  
&emsp;&emsp;&emsp;&emsp;&emsp;_solution_ &larr; cutoff  
&emsp;&emsp;&emsp;__else__  
&emsp;&emsp;&emsp;&emsp;&emsp;__for__ _child_ __in__ successors(_parent_) __do__  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;__if__ _child_ is a goal __then__  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;__return__ _child_  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;add _child_ to __frontier__  
&emsp;__return__  _solution_  

## 3. ITERATIVE-DEEPENING-SEARCH

__function__ ITERATIVE-DEEPENING-SEARCH(_problem_) __returns__ a solution, or failure  
&emsp;__for__ _depth_ = 0 to &infin; __do__  
&emsp;&emsp;&emsp;_result_ &larr; DEPTH\-LIMITED\-SEARCH(_problem_,_depth_)  
&emsp;&emsp;&emsp;__if__ _result_ &ne; cutoff __then return__ _result_
