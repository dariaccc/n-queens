# 4 different algorithms for solving the N-queens problem
## A comparative study on using GA, SA, Hill climbing and DFS to solving the N-queens problem for n <= 200.

The N-queens problem is a known problem, often used in machine learning, that requires placing n queens on an n×n chessboard such that no two queens attack each other. As the problem scales, traditional exhaustive approaches become computationally expensive, making it a useful benchmark for evaluating optimisation strategies.

Below is an example of a 10-queens problem. In the left image, the board is empty. In the center image a false solution is shown, and the queens that are attacking each other are marked. In the right image a solution is shown that was found using the Hill Climbing algorithm.

![10-queens problem. Empty board, false solution, and correct solution](images/chess-boards.png)  


### Depth-First Search
DFS is an exhaustive search algorithm that is the only one of the four algorithms guaranteed to find a solution, but it takes incredibly long. The DFS algorithm can only solve the problem for about n <= 15 in a reasonable amount of time, and as the number n grows the time it takes grows by a tremendous amount.

### Hill climbing
The Hill climbing is the fastest algorithm and can solve for up to n = 100 reliably. It is a local search algorithm and makes moves moving one queen at a time either one step up or one step down.

### Simulated Annealing
The SA is an extention of the HC algorithm, with some added acceptance of bad moves that depend on a temperature. It is by far the most successful algorithm and solved up to n = 200 with approx. 80% accuracy. The local move in the SA is swapping the places of two queens at a time.
The temperature parameter was set to:
- Temperature at start: 1000 for n<100, else 2000
- Temperature coefficient: 0.995

### Genetic Algorithm
The GA required a lot of tuning and took very long to sovle, but also manged to solve for up to n = 200.
Parameters for the GA are:
- Population size: `n * math.log2(n) * 2`
- Maximum generations: 5000
- Mutation rate: 1.5% + 5% every 1000th gen
- Mutation rate if stagnant: 40%
- Crossover method: OX1
- Immigration: Every 10th gen
- Weight & Tournament selection: k=3

The full Overleaf report can be found here: https://www.overleaf.com/read/bknggfkfnqfm#9981ea
