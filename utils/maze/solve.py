from collections import deque
import heapq
import random
from enum import Enum


# ===============================
# Solver Algorithms Supported
# ===============================
class SolveAlgo(Enum):
    BFS = "bfs"
    DFS = "dfs"
    DIJKSTRA = "dijkstra"
    ASTAR = "astar"
    RANDOM_WALK = "random_walk"


# ===============================
# Maze Solver Class
# ===============================
class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.grid = maze.grid
        self.start = maze.start
        self.end = maze.end

        self.wall = maze.wall
        self.path_symbol = "·"   # path marker

    # ----------------------------
    # Helpers
    # ----------------------------
    def _valid_moves(self, r, c):
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.maze.height and 0 <= nc < self.maze.width:
                if self.grid[nr][nc] != self.wall:
                    yield (nr, nc)

    def _reconstruct_path(self, parent):
        path = []
        node = self.end

        while node != self.start:
            path.append(node)
            node = parent[node]

        path.append(self.start)
        path.reverse()
        return path

    def _mark_path(self, path):
        for r, c in path:
            if (r, c) != self.start and (r, c) != self.end:
                self.grid[r][c] = self.path_symbol

    # ===============================
    # 1. BFS Solver (Shortest Path)
    # ===============================
    def _solve_bfs(self):
        queue = deque([self.start])
        parent = {self.start: None}

        while queue:
            node = queue.popleft()

            if node == self.end:
                return self._reconstruct_path(parent)

            for nxt in self._valid_moves(*node):
                if nxt not in parent:
                    parent[nxt] = node
                    queue.append(nxt)

        return None

    # ===============================
    # 2. DFS Solver (Any Path)
    # ===============================
    def _solve_dfs(self):
        stack = [self.start]
        parent = {self.start: None}

        while stack:
            node = stack.pop()

            if node == self.end:
                return self._reconstruct_path(parent)

            for nxt in self._valid_moves(*node):
                if nxt not in parent:
                    parent[nxt] = node
                    stack.append(nxt)

        return None

    # ===============================
    # 3. Dijkstra Solver
    # ===============================
    def _solve_dijkstra(self):
        pq = [(0, self.start)]
        parent = {self.start: None}
        dist = {self.start: 0}

        while pq:
            cost, node = heapq.heappop(pq)

            if node == self.end:
                return self._reconstruct_path(parent)

            for nxt in self._valid_moves(*node):
                new_cost = cost + 1
                if nxt not in dist or new_cost < dist[nxt]:
                    dist[nxt] = new_cost
                    parent[nxt] = node
                    heapq.heappush(pq, (new_cost, nxt))

        return None

    # ===============================
    # 4. A* Solver (Fastest Shortest)
    # ===============================
    def _heuristic(self, a, b):
        # Manhattan Distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _solve_astar(self):
        pq = [(0, self.start)]
        parent = {self.start: None}
        g_score = {self.start: 0}

        while pq:
            _, node = heapq.heappop(pq)

            if node == self.end:
                return self._reconstruct_path(parent)

            for nxt in self._valid_moves(*node):
                temp_g = g_score[node] + 1

                if nxt not in g_score or temp_g < g_score[nxt]:
                    g_score[nxt] = temp_g
                    f_score = temp_g + self._heuristic(nxt, self.end)
                    parent[nxt] = node
                    heapq.heappush(pq, (f_score, nxt))

        return None

    # ===============================
    # 5. Random Walk Solver
    # ===============================
    def _solve_random_walk(self, max_steps=10000):
        node = self.start
        path = [node]


        for _ in range(max_steps):
            if node == self.end:
                return path

            moves = list(self._valid_moves(*node))
            if not moves:
                return None

            node = random.choice(moves)
            path.append(node)

        return None

    # ===============================
    # Main Solve API
    # ===============================
    def solve(self, algo=SolveAlgo.BFS, mark=True):
        if algo == SolveAlgo.BFS:
            path = self._solve_bfs()

        elif algo == SolveAlgo.DFS:
            path = self._solve_dfs()

        elif algo == SolveAlgo.DIJKSTRA:
            path = self._solve_dijkstra()

        elif algo == SolveAlgo.ASTAR:
            path = self._solve_astar()

        elif algo == SolveAlgo.RANDOM_WALK:
            path = self._solve_random_walk()

        else:
            raise ValueError("Unknown solving algorithm")

        if path and mark:
            self._mark_path(path)

        return path
