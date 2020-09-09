class GridWorld():
    def __init__(self, cfg):
        self.cfg = cfg
        self.nrow = nrow = cfg['nrow'];
        self.ncol = ncol = cfg['ncol']
        self.actionset = ['L', 'R', 'U', 'D']
        self.start_state = start_state = self._get_startstate()
        self.goal_state = goal_state = self._get_goalstate()
        if cfg['obstacle_map'] is not None:
            self.obstacle_coords = [(row, col) for row in range(nrow) \
                                    for col in range(ncol) if
                                    cfg['obstacle_map'][row][col] == 1]
        else:
            self.obstacle_coords = []

        self.cost_map = cfg['cost_map']
        if self.cost_map is None:
            self.cost_map = [[None] * ncol] * nrow
        else:
            assert len(self.cost_map) == self.nrow
            assert all([len(i) == self.ncol for i in self.cost_map])
            assert self.cost_map[start_state.coord[0]][
                       start_state.coord[1]] == start_state.cost
            assert self.cost_map[goal_state.coord[0]][
                       goal_state.coord[1]] == goal_state.cost

    def step(self, state, action):
        row, col = state.coord
        next_row, next_col = row, col

        if action == 'L':
            next_col = max(col - 1, 0)
        elif action == 'R':
            next_col = min(col + 1, self.ncol - 1)
        elif action == 'U':
            next_row = max(row - 1, 0)
        elif action == 'D':
            next_row = min(row + 1, self.nrow - 1)
        else:
            raise NotImplementedError(action)

        next_state_coord = (next_row, next_col)
        if next_state_coord in self.obstacle_coords:
            next_state_coord = state.coord

        next_state_cost = self.cost_map[next_state_coord[0]][
            next_state_coord[1]]
        next_state = GridWorldState(next_state_coord, next_state_cost)
        return next_state

    def get_neighborlist(self, state):
        neighborlist = []
        for action in self.actionset:  # "simulate" executing actions
            neighbor = self.step(state, action)
            neighborlist.append((neighbor, action))
        return neighborlist  # list of successors (of the expanded node)

    def estimate_cost_to_go(self, state, heuristic_mode):
        if heuristic_mode == 'zeroed':
            cost_to_go_estimate = 0  # essentialy UniformCostSearch
        elif heuristic_mode == 'manhattan':
            cost_to_go_estimate = abs(self.goal_state.coord[0] - state.coord[0])
            cost_to_go_estimate += abs(
                self.goal_state.coord[1] - state.coord[1])
        else:
            raise NotImplementedError(heuristic_mode)
        return cost_to_go_estimate

    def _get_startstate(self):
        row, col = self.cfg['start_coord']
        cost = 0
        return GridWorldState((row, col), cost)

    def _get_goalstate(self):
        row, col = self.cfg['goal_coord']
        cost = None
        return GridWorldState((row, col), cost)


class GridWorldState():
    def __init__(self, coord, cost):
        assert all([i >= 0 for i in coord])
        self.id = self.coord = coord  # coordinate is in (ith row, jth col)
        self.cost = cost  # a cost of arriving at this state
        self.value_for_priority = 0

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        # Used by PriorityQueue()
        # Assume: the lower the value, the higher the priority
        return self.value_for_priority < other.value_for_priority
