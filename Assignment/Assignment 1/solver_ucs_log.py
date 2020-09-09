#!/usr/bin/python
import sys

from laser_tank import LaserTankMap

import queue
import time

"""
Template file for you to implement your solution to Assignment 1.

COMP3702 2020 Assignment 1 Support Code

@author: Anindya Sarup (44243726)
"""


class LaserTankState(LaserTankMap):

    def __init__(self, x_size, y_size, grid_data, player_x, player_y,
                 player_heading, cost):
        super().__init__(x_size, y_size, grid_data, player_x, player_y,
                         player_heading)
        # TODO: is there an alternative to solve the hashing issue ?
        self.id = (player_x, player_y, player_heading,
                   tuple(map(tuple, self.grid_data)))
        self.cost = cost
        self.total_cost = cost

    def step(self, move):
        next_player_x = self.player_x
        next_player_y = self.player_y
        next_player_heading = self.player_heading
        next_grid_data = [row[:] for row in self.grid_data]

        dummy_map = LaserTankState(self.x_size, self.y_size, next_grid_data,
                                   player_x=self.player_x,
                                   player_y=self.player_y,
                                   player_heading=self.player_heading, cost=1)

        if dummy_map.apply_move(move) == dummy_map.SUCCESS:
            next_grid_data = dummy_map.grid_data
            next_player_x = dummy_map.player_x
            next_player_y = dummy_map.player_y
            next_player_heading = dummy_map.player_heading
        else:
            next_grid_data = [row[:] for row in self.grid_data]

        next_map_state = LaserTankState(self.x_size, self.y_size,
                                        next_grid_data,
                                        player_x=next_player_x,
                                        player_y=next_player_y,
                                        player_heading=next_player_heading,
                                        cost=1)

        return next_map_state

    def estimate_cost_to_go(self, goal, heuristic_mode=None):
        cost_to_go_estimate = 0  # specifying no mode leads to UCS Algorithm
        if heuristic_mode == "manhattan":
            # TODO: are the coordinates for the goal in the correct order?
            cost_to_go_estimate = abs(goal[0] - self.player_x)
            cost_to_go_estimate += abs(goal[1] - self.player_y)
        return cost_to_go_estimate

    def __eq__(self, other):
        # return self.player == other.player and self.grid_data ==
        # other.grid_data
        return self.id == other.id

    def __lt__(self, other):
        return self.total_cost < other.total_cost


def a_star_algorithm(game_map, flag_coords):
    actions = []
    moves_set = game_map.MOVES

    start = LaserTankState(game_map.x_size, game_map.y_size, game_map.grid_data,
                           game_map.player_x, game_map.player_y,
                           game_map.player_heading, cost=1)

    fringe = queue.PriorityQueue()
    fringe.put(start)

    explored = {start.id: start.cost}
    path = {start.id: []}

    log = {}

    node_counter = 1

    while not fringe.empty():
        current = fringe.get()
        if current.is_finished():
            actions = path[current.id]
            log['number of steps for optimal answer'] = len(actions)
            log['total number of nodes'] = node_counter
            log['total number of nodes in fringes (reached goal)'] = \
                fringe.qsize()
            log['total number of nodes in the explored list'] = len(explored)
            break
        for move in moves_set:
            neighbour = current.step(move)
            cost_so_far = explored[current.id] + current.cost
            node_counter += 1
            if (neighbour.id not in explored) or \
                    (cost_so_far < explored[neighbour.id]):
                explored[neighbour.id] = cost_so_far
                path[neighbour.id] = path[current.id] + [move]
                value_for_priority = cost_so_far + \
                                     neighbour.estimate_cost_to_go(flag_coords)
                neighbour.total_cost = value_for_priority
                fringe.put(neighbour)

    return actions, log


def write_output_file(filename, actions, log):
    """
    Write a list of actions to an output file. You should use this method to write your output file.
    :param filename: name of output file
    :param actions: list of actions where is action is in LaserTankMap.MOVES
    """
    f = open(filename, 'w')

    for i in range(len(actions)):
        f.write(str(actions[i]))
        if i < len(actions) - 1:
            f.write(',')
    f.write('\n')

    for k in log.keys():
        f.write(str(k) + ' = ' + str(log.get(k)))
        f.write('\n')

    f.close()


def main(arglist):
    input_file = arglist[0]
    output_file = arglist[1]

    # Read the input testcase file
    game_map = LaserTankMap.process_input_file(input_file)

    flag_coords = [(col, row) for row in range(game_map.y_size)
                   for col in range(game_map.x_size)
                   if game_map.grid_data[row][col] == game_map.FLAG_SYMBOL][0]

    start = time.time()

    # Run a-star algorithm
    actions, log = a_star_algorithm(game_map=game_map, flag_coords=flag_coords)

    end = time.time() - start

    log['run time of the algorithm'] = end
    # Write the solution to the output file
    write_output_file(output_file, actions, log)


if __name__ == '__main__':
    main(sys.argv[1:])
