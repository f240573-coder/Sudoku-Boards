import copy

# Count statistics
bt_calls_count = 0
fail_count = 0

# Read Sudoku from file
def load_puzzle(file_path):
    puzzle = []
    with open(file_path, 'r') as file:
        for line in file:
            puzzle.append([int(val) for val in line.strip()])
    return puzzle

# Get neighbors of a cell
def fetch_neighbors(r, c):
    neigh = set()

    # Row and Column
    for idx in range(9):
        neigh.add((r, idx))
        neigh.add((idx, c))

    # 3x3 grid
    box_r = (r // 3) * 3
    box_c = (c // 3) * 3

    for i in range(3):
        for j in range(3):
            neigh.add((box_r + i, box_c + j))

    neigh.remove((r, c))
    return neigh

# Initialize domains
def setup_domains(puzzle):
    doms = {}
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == 0:
                doms[(r, c)] = set(range(1, 10))
            else:
                doms[(r, c)] = {puzzle[r][c]}
    return doms

# AC-3 Algorithm
def apply_ac3(doms):
    arc_queue = [(a, b) for a in doms for b in fetch_neighbors(*a)]

    while arc_queue:
        a, b = arc_queue.pop(0)
        if revise_arc(doms, a, b):
            if len(doms[a]) == 0:
                return False
            for k in fetch_neighbors(*a):
                if k != b:
                    arc_queue.append((k, a))
    return True

def revise_arc(doms, a, b):
    changed_flag = False
    for v in set(doms[a]):
        if all(v == other for other in doms[b]):
            doms[a].remove(v)
            changed_flag = True
    return changed_flag

# Check consistency
def check_valid(doms, variable, val):
    for neigh in fetch_neighbors(*variable):
        if len(doms[neigh]) == 1 and val in doms[neigh]:
            return False
    return True

# Forward checking
def do_forward(doms, variable, val):
    temp = copy.deepcopy(doms)
    temp[variable] = {val}

    for neigh in fetch_neighbors(*variable):
        if val in temp[neigh]:
            temp[neigh].remove(val)
            if len(temp[neigh]) == 0:
                return None
    return temp

# Select unassigned variable
def pick_unassigned(doms):
    for variable in doms:
        if len(doms[variable]) > 1:
            return variable
    return None

# Backtracking
def run_backtrack(doms):
    global bt_calls_count, fail_count
    bt_calls_count += 1

    variable = pick_unassigned(doms)
    if variable is None:
        return doms

    for val in doms[variable]:
        if check_valid(doms, variable, val):
            new_doms = do_forward(doms, variable, val)
            if new_doms:
                result = run_backtrack(new_doms)
                if result:
                    return result

    fail_count += 1
    return None

# Solve Sudoku
def solve_puzzle(file_path):
    global bt_calls_count, fail_count
    bt_calls_count = 0
    fail_count = 0

    puzzle = load_puzzle(file_path)
    doms = setup_domains(puzzle)

    apply_ac3(doms)
    result = run_backtrack(doms)

    print("Solution:")
    for r in range(9):
        row_vals = []
        for c in range(9):
            row_vals.append(list(result[(r, c)])[0])
        print(row_vals)

    print("Backtrack Calls:", bt_calls_count)
    print("Failures:", fail_count)

# Example
print("=== EASY ===")
solve_puzzle("board1.txt")
print("\n=== MEDIUM ===")
solve_puzzle("board2.txt")
print("\n=== HARD ===")
solve_puzzle("board3.txt")
print("\n=== VERY HARD ===")
solve_puzzle("board5.txt")