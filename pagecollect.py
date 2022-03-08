from search import *
import time

#################
# Problem class #
#################


class PageCollect(Problem):

    def __init__(self, initial):

        # create goal state
        goal = []
        for row in initial.grid:
            new_row = []
            for element in row:
                if element == 'p' or element == '@':
                    new_row.append(' ')
                elif element == 'X':
                    new_row.append('@')
                else:
                    new_row.append(element)
            goal.append(tuple(new_row))
        goal = State(tuple(goal))

        super().__init__(initial, goal)

    def actions(self, state):

        irow, icol = state.student_position

        if state.grid[irow][icol-1] != '#':
            yield 'west'
        if state.grid[irow+1][icol] != '#':
            yield 'south'
        if state.grid[irow][icol+1] != '#':
            yield 'east'
        if state.grid[irow-1][icol] != '#':
            yield 'north'

    def result(self, state, action):

        irow, icol = state.student_position
        new_grid = list(state.grid)
        new_grid[irow] = list(state.grid[irow])
        new_grid[irow][icol] = ' '

        if action == 'west' or action == 'east':
            new_grid[irow][icol-1 if action == 'west' else icol+1] = '@'

        if action == 'north' or action == 'south':
            new_x = irow-1 if action == 'north' else irow+1
            new_grid[new_x] = list(state.grid[new_x])
            new_grid[new_x][icol] = '@'
            new_grid[new_x] = tuple(new_grid[new_x])

        new_grid[irow] = tuple(new_grid[irow])
        new_grid = tuple(new_grid)
        return State(new_grid)

    def h(self, node: Node):
        return 0
        try:
            problem = PageCollectHeuristic.load(node)
            h_node = uniform_cost_search(problem)
            return h_node.path_cost
        except ValueError:
            return 0

    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()

        state = State.from_string(''.join(lines))
        return PageCollect(state)


class PageCollectHeuristic(Problem):

    def __init__(self, graph: dict, initial):
        self.graph = graph
        super().__init__(initial, 'examiner')

    def actions(self, state):
        return self.graph[state].keys()

    def result(self, state, action):
        return action

    def path_cost(self, c, state1, action, state2):
        return self.graph[state1][state2]

    def load(node: Node):

        # {
        #   'student': {
        #       'page0': 10,
        #       'page1': 20,
        #       'examiner': 15
        #   },
        #   'page0': {
        #       'page1': 6
        #   },
        #   'page1': {
        #       'page0': 6
        #   },
        #   'examiner': {}
        # }

        student_row, student_col = node.state.student_position
        examiner_row, examiner_col = node.state.examiner_position
        pages_positions = node.state.pages_positions

        graph = dict()
        graph['student'] = dict()
        graph['student']['examiner'] = abs(
            student_row-examiner_row) + abs(student_col-examiner_col)

        for i, (page_row, page_col) in enumerate(pages_positions):
            graph['student'][f'page{i}'] = abs(
                student_row-page_row) + abs(student_col-page_col)
            graph[f'page{i}'] = dict()
            for j, (page2_row, page2_col) in enumerate(pages_positions):
                if i == j:
                    continue
                graph[f'page{i}'][f'page{j}'] = abs(
                    page2_row-page_row) + abs(page2_col-page_col)

        graph['examiner'] = dict()

        # print(graph)

        return PageCollectHeuristic(graph, 'student')

###############
# State class #
###############


class State:
    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid

    @property
    def student_position(self):
        for irow in range(0, self.nbr):
            for icol in range(0, self.nbc):
                if self.grid[irow][icol] == '@':
                    return (irow, icol)
        raise ValueError('No student in the grid')

    @property
    def examiner_position(self):
        for irow in range(0, self.nbr):
            for icol in range(0, self.nbc):
                if self.grid[irow][icol] == 'X':
                    return (irow, icol)
        raise ValueError('No examiner in the grid')

    @property
    def pages_positions(self):
        pages = []
        for irow in range(0, self.nbr):
            for icol in range(0, self.nbc):
                if self.grid[irow][icol] == 'p':
                    pages.append((irow, icol))
        return pages

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other_state):
        return self.grid == other_state.grid

    def __hash__(self):
        return hash(self.grid)

    def __lt__(self, other):
        return hash(self) < hash(other)

    def from_string(string):
        lines = string.strip().splitlines()
        return State(tuple(
            map(lambda x: tuple(x.strip()), lines)
        ))


#####################
# Launch the search #
#####################
problem = PageCollect.load(sys.argv[1])

start_timer = time.perf_counter()
node, nb_explored = astar_search(problem)
end_timer = time.perf_counter()

print("* Execution time:\t", str(end_timer - start_timer))
print("* Path cost to goal:\t", node.depth, "moves")
print("* #Nodes explored:\t", nb_explored)

# example of print
path = node.path()

# print('Number of moves: ' + str(node.depth))
# for n in path:
#     # assuming that the __str__ function of state outputs the correct format
#     print(n.state)
#     print()
