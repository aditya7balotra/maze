import random
from enum import Enum


# ===============================
# Maze Algorithms Supported
# ===============================
class MazeAlgo(Enum):
    DFS = "dfs"
    PRIM = "prim"
    KRUSKAL = "kruskal"
    WILSON = "wilson"
    ALDOUS = "aldous"
    DIVISION = "division"
    RANDOM = "random"


# ===============================
# Maze Class
# ===============================
class Maze:
    def __init__(
        self,
        width=21,
        height=21,
        wall="#",
        path=" ",
        start_symbol="S",
        end_symbol="E",
    ):
        if width % 2 == 0 or height % 2 == 0:
            raise ValueError("Width and Height must be odd numbers!")

        self.width = width
        self.height = height

        self.wall = wall
        self.path = path
        self.start_symbol = start_symbol
        self.end_symbol = end_symbol

        self.start = (1, 1)
        self.end = (height - 2, width - 2)

        self.reset()

    # ----------------------------
    # Reset Maze Grid
    # ----------------------------
    def reset(self):
        self.grid = [[self.wall for _ in range(self.width)] for _ in range(self.height)]

    # ----------------------------
    # Helpers
    # ----------------------------
    def _in_bounds(self, r, c):
        return 0 < r < self.height - 1 and 0 < c < self.width - 1

    def _set_path(self, r, c):
        self.grid[r][c] = self.path

    def _neighbors(self, r, c):
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        result = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if self._in_bounds(nr, nc):
                result.append((nr, nc, dr // 2, dc // 2))
        return result

    # ===============================
    # 1. DFS Backtracker
    # ===============================
    def _generate_dfs(self):
        stack = [self.start]
        self._set_path(*self.start)

        while stack:
            r, c = stack[-1]
            unvisited = [
                (nr, nc, mr, mc)
                for nr, nc, mr, mc in self._neighbors(r, c)
                if self.grid[nr][nc] == self.wall
            ]

            if unvisited:
                nr, nc, mr, mc = random.choice(unvisited)
                self._set_path(r + mr, c + mc)
                self._set_path(nr, nc)
                stack.append((nr, nc))
            else:
                stack.pop()

    # ===============================
    # 2. Prim’s Algorithm
    # ===============================
    def _generate_prim(self):
        self._set_path(*self.start)
        walls = []

        r, c = self.start
        for nr, nc, mr, mc in self._neighbors(r, c):
            walls.append((nr, nc, mr, mc, r, c))

        while walls:
            nr, nc, mr, mc, r, c = random.choice(walls)
            walls.remove((nr, nc, mr, mc, r, c))

            if self.grid[nr][nc] == self.wall:
                self._set_path(r + mr, c + mc)
                self._set_path(nr, nc)

                for nnr, nnc, mmr, mmc in self._neighbors(nr, nc):
                    if self.grid[nnr][nnc] == self.wall:
                        walls.append((nnr, nnc, mmr, mmc, nr, nc))

    # ===============================
    # 3. Kruskal’s Algorithm
    # ===============================
    def _generate_kruskal(self):
        parent = {}

        def find(cell):
            while parent[cell] != cell:
                parent[cell] = parent[parent[cell]]
                cell = parent[cell]
            return cell

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        cells = []
        edges = []

        for r in range(1, self.height, 2):
            for c in range(1, self.width, 2):
                cell = (r, c)
                parent[cell] = cell
                cells.append(cell)

                for nr, nc, mr, mc in self._neighbors(r, c):
                    if (nr, nc) in parent:
                        edges.append((cell, (nr, nc), (r + mr, c + mc)))

        random.shuffle(edges)

        for a, b, wall_cell in edges:
            if find(a) != find(b):
                union(a, b)
                self._set_path(*a)
                self._set_path(*b)
                self._set_path(*wall_cell)

    # ===============================
    # 4. Wilson’s Algorithm
    # ===============================
    def _generate_wilson(self):
        unvisited = {(r, c) for r in range(1, self.height, 2)
                     for c in range(1, self.width, 2)}

        first = random.choice(list(unvisited))
        unvisited.remove(first)
        self._set_path(*first)

        while unvisited:
            cell = random.choice(list(unvisited))
            path = [cell]

            while cell in unvisited:
                r, c = cell
                nr, nc, mr, mc = random.choice(self._neighbors(r, c))
                cell = (nr, nc)

                if cell in path:
                    path = path[:path.index(cell) + 1]
                else:
                    path.append(cell)

            for i in range(len(path) - 1):
                r1, c1 = path[i]
                r2, c2 = path[i + 1]
                self._set_path(r1, c1)
                self._set_path(r2, c2)
                self._set_path((r1 + r2) // 2, (c1 + c2) // 2)

                if path[i] in unvisited:
                    unvisited.remove(path[i])

    # ===============================
    # 5. Aldous–Broder Algorithm
    # ===============================
    def _generate_aldous(self):
        cells = [(r, c) for r in range(1, self.height, 2)
                 for c in range(1, self.width, 2)]

        visited = set()
        current = random.choice(cells)
        visited.add(current)
        self._set_path(*current)

        while len(visited) < len(cells):
            r, c = current
            nr, nc, mr, mc = random.choice(self._neighbors(r, c))
            next_cell = (nr, nc)

            if next_cell not in visited:
                self._set_path(r + mr, c + mc)
                self._set_path(*next_cell)
                visited.add(next_cell)

            current = next_cell

    # ===============================
    # 6. Recursive Division
    # ===============================
    def _generate_division(self):

        def divide(x, y, w, h):
            if w < 3 or h < 3:
                return

            horizontal = w < h
            if horizontal:
                row = y + random.randrange(2, h, 2)
                hole = x + random.randrange(1, w, 2)

                for i in range(x, x + w):
                    if i != hole:
                        self.grid[row][i] = self.wall

                divide(x, y, w, row - y)
                divide(x, row + 1, w, y + h - row - 1)

            else:
                col = x + random.randrange(2, w, 2)
                hole = y + random.randrange(1, h, 2)

                for i in range(y, y + h):
                    if i != hole:
                        self.grid[i][col] = self.wall

                divide(x, y, col - x, h)
                divide(col + 1, y, x + w - col - 1, h)

        # Fill with paths first
        for r in range(self.height):
            for c in range(self.width):
                self.grid[r][c] = self.path

        # Border walls
        for r in range(self.height):
            self.grid[r][0] = self.wall
            self.grid[r][-1] = self.wall
        for c in range(self.width):
            self.grid[0][c] = self.wall
            self.grid[-1][c] = self.wall

        divide(1, 1, self.width - 2, self.height - 2)

    # ===============================
    # 7. Random Noise Fill
    # ===============================
    def _generate_random(self, density=0.7):
        for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
                self.grid[r][c] = self.path if random.random() < density else self.wall

    # ===============================
    # Generate Maze Main API
    # ===============================
    def generate(self, algo=MazeAlgo.DFS):
        self.reset()

        if algo == MazeAlgo.DFS:
            self._generate_dfs()
        elif algo == MazeAlgo.PRIM:
            self._generate_prim()
        elif algo == MazeAlgo.KRUSKAL:
            self._generate_kruskal()
        elif algo == MazeAlgo.WILSON:
            self._generate_wilson()
        elif algo == MazeAlgo.ALDOUS:
            self._generate_aldous()
        elif algo == MazeAlgo.DIVISION:
            self._generate_division()
        elif algo == MazeAlgo.RANDOM:
            self._generate_random()
        else:
            raise ValueError("Unknown algorithm")

        # Place Start/End
        sr, sc = self.start
        er, ec = self.end
        self.grid[sr][sc] = self.start_symbol
        self.grid[er][ec] = self.end_symbol

    # ===============================
    # Save Maze
    # ===============================
    def save_to_file(self, filename="maze.txt"):
        with open(filename, "w") as f:
            for row in self.grid:
                f.write("".join(row) + "\n")

        print("✅ Maze saved to", filename)

    # ===============================
    # Display Maze
    # ===============================
    def display(self):
        for row in self.grid:
            print("".join(row))


# ===============================
# Example Run
# ===============================
if __name__ == "__main__":
    maze = Maze(31, 31)

    maze.generate(MazeAlgo.PRIM)
    maze.display()

    maze.save_to_file("prim_maze.txt")
