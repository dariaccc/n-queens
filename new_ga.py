import random
import math
from numba import njit, prange, config
import numpy as np
import tracemalloc
import time

config.NUMBA_NUM_THREADS = 4

nr_queens = int(input("Number of queens: "))
if nr_queens < 4:
    print("No solutions for fewer than 4 queens.")

print(f"input received: {nr_queens}")

@njit(parallel=True)
def batch_fitness(pop):
    n = len(pop)
    out = np.zeros(n, dtype=np.int32)
    for i in prange(n):
        q = pop[i]
        d1 = np.zeros(2 * len(q), dtype=np.int32)
        d2 = np.zeros(2 * len(q), dtype=np.int32)
        for col in range(len(q)):
            r = q[col]
            d1[col + r] += 1
            d2[col - r + len(q)] += 1
        att = 0
        for count in d1:
            if count > 1:
                att += count * (count - 1) // 2
        for count in d2:
            if count > 1:
                att += count * (count - 1) // 2
        out[i] = att
    return out





#initialisation
pop_size = 600 if nr_queens < 100 else 1500 if nr_queens == 100 else 2000
max_gen = 7000 if nr_queens < 100 else 12000 if nr_queens == 100 else 20000

gen = np.array([np.random.permutation(nr_queens) for _ in range(pop_size)], dtype=np.int32)  #

# === TOURNAMENT SELECTION: CHANGE ===
# Avoid repeated conversion and use numpy arrays internally
def tournament_selection(gen, fit_list, k=3):
    idxs = np.random.choice(len(gen), k, replace=False)
    best_idx = idxs[np.argmin(fit_list[idxs])]
    return gen[best_idx]


# === CROSSOVER: BIG CHANGE to speed up child creation ===
def crossover(gen, fit_list, its):
    new_gen = []

    #elitism - keep the best parents to the next generation
    top_int = int(len(fit_list) * 0.15)
    sorted_indices = np.argsort(fit_list)
    for i in sorted_indices[:top_int]:
        new_gen.append(gen[i])

    # Introduce random chromosomes more frequently for exploration
    if its % 10 == 0:
        for _ in range(5):
            new_gen.append(np.random.permutation(nr_queens))

    while len(new_gen) < len(gen):
        p1 = tournament_selection(gen, fit_list, k=3)
        p2 = tournament_selection(gen, fit_list, k=3)

        size = len(p1)
        start = random.randint(0, size - 2)
        end = random.randint(start + 1, size - 1)

        child = np.full(size, -1, dtype=np.int32)
        child[start:end+1] = p1[start:end+1]

        # Instead of set, use a boolean mask for faster lookups
        used = np.zeros(nr_queens, dtype=bool)
        used[child[start:end+1]] = True

        pos = (end + 1) % size
        for gene in p2:
            if not used[gene]:
                child[pos] = gene
                used[gene] = True
                pos = (pos + 1) % size

        mutate(child)
        new_gen.append(child)

    new_fit = batch_fitness(np.array(new_gen, dtype=np.int32))

    return np.array(new_gen, dtype=np.int32), new_fit

# === MUTATE: simplify to single swap with fixed mutation rate ===
def mutate(child):
    if stagnant_gens > 100:
        mut_rate = 0.4
    else:
        mut_rate = min(0.15 + (its // 1000) * 0.05, 0.3)

    if random.random() < mut_rate:
        pos1 = random.randint(0, len(child) - 1)
        pos2 = random.randint(0, len(child) - 1)
        child[pos1], child[pos2] = child[pos2], child[pos1]

def check_sol(fit_list):
    for idx, i in enumerate(fit_list):
        if i == 0:
            return True, idx
    return False, -1

# === RUN GA ===
print("starting...")
tracemalloc.start()
start = time.time()

fit_list = batch_fitness(gen)

best_fitness = min(fit_list)
stagnant_gens = 0
print(f"Starting fitness: {best_fitness}")

its = 0
x = False
restart_used = False

while not x and its < max_gen:
    gen, fit_list = crossover(gen, fit_list, its)

    prev_best = best_fitness
    best_fitness = min(fit_list)

    if best_fitness == prev_best:
        stagnant_gens += 1
        if stagnant_gens >= 300 and not restart_used:
            print(f"[Stagnation] Reinitializing bottom 25% at gen {its}")
            quarter = len(gen) // 4
            worst_indices = np.argsort(fit_list)[-quarter:]
            for i in worst_indices:
                gen[i] = np.random.permutation(nr_queens)
            fit_list = batch_fitness(gen)
            stagnant_gens = 0
            restart_used = True #will only restart once - mass immigration to avoid stagnation
    else:
        stagnant_gens = 0

    if its % 500 == 0 and its > 0:
        current = time.time()
        cur_elapsed = current - start
        print(f"Iteration {its}, best fitness: {best_fitness}")

    x, idx = check_sol(fit_list)
    its += 1

if x:
    print(f"Solution found at generation {its}, index {idx}")
    print(f"Solution: {(gen[idx] + 1).tolist()}")  # +1 for human-friendly output
else:
    print(f"No solution found after {its} generations.")

current, peak = tracemalloc.get_traced_memory()
print(f"Peak memory usage: {peak / 10**6:.2f} MB")

tracemalloc.stop()
end = time.time()

elapsed = end - start
print(f"Elapsed time: {elapsed:.2f} seconds")