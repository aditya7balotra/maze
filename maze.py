from utils.maze.create import MazeAlgo, Maze
from utils.maze.solve import SolveAlgo, MazeSolver
import random as rnd
import itertools
import pandas as pd

def create_maze(width, height,
                wall = "#",
                path = " ", 
                start = "S", 
                end = "E",
                csv_fname = "maze.csv",
                datalen = 10):

    m = Maze(width, 
            height, 
            wall= wall, 
            path= path, 
            start_symbol= start, 
            end_symbol= end
            )
    
    df = pd.DataFrame(columns= [f"input{i}" for i in range(width * height)] + ["sol_moves"])

    solveAlgos = [SolveAlgo.ASTAR, SolveAlgo.BFS, SolveAlgo.DFS, SolveAlgo.DIJKSTRA]
    
    algos = [MazeAlgo.ALDOUS, MazeAlgo.DFS, MazeAlgo.DIVISION, MazeAlgo.KRUSKAL, MazeAlgo.PRIM, MazeAlgo.WILSON]
    created = 0
    while (created != datalen):
        m.generate(algo= rnd.choice(algos))
        grid = list(itertools.chain.from_iterable(m.grid))
        sol = MazeSolver(m)
        sol_moves = sol.solve(algo= rnd.choice(solveAlgos))
        if sol_moves is None:
            continue
        # print(sol_moves, "iter")
        sols = ""
        for i in sol_moves:
            sols += str(i) + "|"
        # print(len(df))
        data = grid + [sols]
        df.loc[len(df)] = data
        created += 1
        print(f"Progress... {created/datalen}", end= "\r")    
    
    df.to_csv(csv_fname)
    
    
create_maze(11, 11, datalen= 10000)