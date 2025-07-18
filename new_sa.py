#imports
import random
import math
from numba import njit, prange # library to decrease computation time for the fitness function
import numpy as np #numpy can make fitness into arrays for faster computation
from multiprocessing import Pool #for parallel processing of the fitness function
import tracemalloc #for comparing memory usage among algorithms
import time

#input for the amount of queens
nr_queens = int(input("Number of queens: "))
if nr_queens < 4:
    print("There are no solutions for the n-queens problem for fewer queens than 4")
print(f"Number of queens: {nr_queens}")

#initialisation with random queens

def random_q(nr_queens):
    queens = list(range(1, nr_queens + 1))  # columns from 1 to n
    random.shuffle(queens)  # random permutation ensures no duplicate columns
    return queens

queens = random_q(nr_queens)
print(f"Initial queens placements: {queens}")

#fitness for all other functions

@njit

#for only diagonal moves
#rewriting to arrays for even faster computation

def fitness(queens):
    n = len(queens)
    diag1 = np.zeros(2 * n, dtype=np.int32)
    diag2 = np.zeros(2 * n, dtype=np.int32)

    for col in range(n):
        r = queens[col]
        d1 = col + r
        d2 = col - r + n  #offset to keep index non-negative

        diag1[d1] += 1
        diag2[d2] += 1

    attacks = 0
    for count in diag1:
        if count > 1:
            attacks += count * (count - 1) // 2
    for count in diag2:
        if count > 1:
            attacks += count * (count - 1) // 2

    return attacks

print(f"Inital fitness {fitness(queens)}")

#simulated annealing
start = time.time()
tracemalloc.start()

loop = 0
restarts = 0
no_change = 0

#initialize board
queens = random_q(nr_queens)
best_queens = queens[:]
best_fit = fitness(queens)

#higher initial temperature for higher values of n
temp = 1000 if nr_queens < 100 else 2000
x = True

while x:
    old_fitness = fitness(queens)

    #swap 2 queens (1 local move)
    pos1 = random.randint(0, len(queens) - 1)
    pos2 = random.randint(0, len(queens) - 1)
    while pos2 == pos1:
        pos2 = random.randint(0, len(queens) - 1)

    #swap the rows (rows = values in the list)
    queens[pos1], queens[pos2] = queens[pos2], queens[pos1]

    new_fit = fitness(queens)
    delta = new_fit - old_fitness

    if delta <= 0:
        pass  #accept better or equal move
    else:
        prob = math.exp(-delta / temp)
        if random.random() >= prob:
            # reject move, revert swap
            queens[pos1], queens[pos2] = queens[pos2], queens[pos1]
            
    #update best solution

    if new_fit < best_fit:
        best_fit = new_fit
        best_queens = queens[:]
        no_change = 0
    else:
        no_change += 1

    #success
    if new_fit == 0:
        x = False

    #restart if stuck
    if no_change > 2000 and best_fit > 10:
        queens = random_q(nr_queens)
        temp = 1000
        restarts += 1
        no_change = 0
        if restarts > 1000:
            x = False

    loop += 1
    temp *= 0.995

print(loop)
print(f"Restarts: {restarts}")

attacks = fitness(best_queens)
if attacks > 0:
    print(f"No solution found, best: {best_queens}, with {attacks} attacks")
else:
    print(f"Solution: {best_queens}")

current, peak = tracemalloc.get_traced_memory()
print(f"Peak memory usage: {peak / 10**6:.2f} MB")

tracemalloc.stop()
end = time.time()

elapsed = end - start
print(f"Elapsed time: {elapsed:.2f} seconds")