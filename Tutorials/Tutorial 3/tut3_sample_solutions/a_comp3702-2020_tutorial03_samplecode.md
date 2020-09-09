# comp3702-2020_tutorial03_samplecode.md
* This is merely a sample code that prioritizes pedagogical benefits over
  code efficiency, advance programming techniques, advance language features, and etc.
* Please report any bug to the teaching team, thank you.

# How to use
* Download this gist's zip using `Download ZIP` button in the top right corner of this page.
* Extract everything insize that zip to `your_directory`
* Type `python3 your_directory/question_3_1.py`
* Type `python3 your_directory/question_3_2.py`
* Select any sub-question by modifying the main question files, namely
  [question_3_1.py](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-question_3_1-py), and
  [question_3_2.py](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-question_3_2-py)

# Attacking strategy (Q1, Q2)
* Skim Q1 and Q2, try to map what is required for designing (modeling)
  agent and environment interaction.
  What is the agent? What is the environment? What is the agent's goal?
  What is the state set? What is the action set?
  What is the state transition function? What is the utility (reward) function?
  Recall by model, we mean the MDP (as the "calculus" of autonomous decision making).
  Refer to Tutorial 1.
* Structure the code into 3 modules, ie `experiment`, `agent` and `environment`.
  Follow the top-down approach.
  * experiment codes
    * [question_3_1.py](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-question_3_1-py)
    * [question_3_2.py](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-question_3_2-py)
  * (searching) agent codes
    * [breath_first_search.py](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-breath_first_search-py)
    * [depth_first_search.py](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-depth_first_search-py)
    * [iterative_deepening_search.py](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-iterative_deepening_search-py)
    * [astar_search.py](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-astar_search-py)
  * environment codes
    * [gridworld.py](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py)

## Experiment codes
* Idenfity what kinds of information that we should log
* Design the logging mechanism

## Searching agent codes
* Re-use BFS, DFS, and UCS from Tutorial 2
* Build IDDFS on top of DFS
  * https://eddmann.com/posts/using-iterative-deepening-depth-first-search-in-python/
  * https://www.geeksforgeeks.org/iterative-deepening-searchids-iterative-deepening-depth-first-searchiddfs/
  * Iterative Deepening Depth First Search, Douglas Fisher
    * https://www.youtube.com/watch?v=7QcoJjSVT38
    * https://www.youtube.com/watch?v=5MpT0EcOIyM
* Build A* on top of UCS
  * think of some admissible heuristics
* Recall the common ingredients of search agents
  * data structure (container)
  * goal state checker
  * a way to obtain the neighbors (successors) of the currently explored (expanded) state

## Environment codes
* Two reasonable classes:
  [`GridWorld`](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py-L1), and
  [`GridWorldState`](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py-L68).
* Class [`GridWorld`](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py-L1)
  provides
  * [`step(self, state, action)`](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py-L23)
    encodes the dynamics (the state transition) of this environment.
    * This is used for, eg getting the neighbors of a state.
  * [`get_neighborlist(self, state)`](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py-L41)
    identifies the neighbors of any given `state`.
    * It "simulates" the interaction by calling the `step()` function.
  * [`estimate_cost_to_go(self, state, heuristic_mode)`](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py-L48)
    provides some heuristics for informed search algorithms.
    * Recall that a heuristic is essentially an estimate of the cost-to-go from a state.
    * Some may prefer treating this as part of the agent module.
  * [`__init__(self, cfg)`](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py-L2),
    which is the class' constructor, handles
    * setup (initialization) based on the configuration `cfg`
    * some sanity checks for a valid enviroment instance.
* Class [`GridWorldState`](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py-L68)
  provides
  * state equality check:
    [`__eq__(self, other)`](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py-L75)
  * state prioritization for, eg Priority Queue:
    [`__lt__(self, other)`](https://gist.github.com/tttor/826be15b99bb4b33a50787d7eb7b5fda#file-gridworld-py-L78)


