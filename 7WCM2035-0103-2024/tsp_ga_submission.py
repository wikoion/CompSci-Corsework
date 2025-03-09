import random
import math
import copy
import matplotlib.pyplot as plt
import numpy as np
import time

NUM_GENERATIONS = 100
NUM_PATHS = 100
GRID_SIZE = 100
NUM_LOCATIONS = 10
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.2
NUM_TOURNAMENT_SELECTION = 10
NUM_EXECUTIONS = 10

def main():
    initial_population = gen_paths(NUM_PATHS, GRID_SIZE, NUM_LOCATIONS)

    best_scored_path = ()
    start = time.time()
    for i in range(1, NUM_EXECUTIONS):
        it_start = time.time()
        ga = genetic_algorithm(initial_population, CROSSOVER_RATE, MUTATION_RATE, NUM_GENERATIONS, NUM_TOURNAMENT_SELECTION)
        scored_path = add_path_scores(ga)[0]

        if len(best_scored_path) == 0:
            best_scored_path = scored_path
        elif scored_path[0] < best_scored_path[0]:
            best_scored_path = scored_path

        it_end = time.time()
        print("Best path from run ", i, "elapsed time:", it_end-it_start, "seconds")
        print_scored_paths([scored_path])

    end = time.time()

    print("Best path in ", NUM_EXECUTIONS, " executions, total elapsed time:", end-start, "seconds")
    print_scored_paths([best_scored_path])
    plot_best_path(best_scored_path)

def plot_best_path(best_scored_path):
    total_score = best_scored_path[0]
    best_path = np.array(best_scored_path[1])
    
    best_path = np.vstack([best_path, best_path[0]])  

    plt.figure(figsize=(8, 6))
    plt.plot(best_path[:, 0], best_path[:, 1], 'o-', linestyle="-", color="b", label='TSP Path')
    plt.scatter(best_path[:, 0], best_path[:, 1], color="r", marker="o", label="Cities")

    for i, (x, y) in enumerate(best_path):
        if i < len(best_path) -1:
            x1, y1 = best_path[i]
            x2, y2 = best_path[i + 1]
            plt.text(x, y, str(i), fontsize=12, ha='right')

            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            distance = round(math.hypot(x2 - x1, y2 - y1))
            plt.text(mid_x, mid_y, str(distance), fontsize=10, ha='center', color="green")

    plt.xticks([])
    plt.yticks([])

    plt.title(f"TSP Solution (Total Distance: {total_score})", fontsize=14)
    plt.legend()
    plt.show()

# Generation logic copied from rubrick
def gen_path(grid_size, num_locations):
    locations_to_visit = set()

    while len(locations_to_visit) < num_locations:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)

        locations_to_visit.add((x, y))

    locations_to_visit = list(locations_to_visit)
    return locations_to_visit

def gen_paths(num_paths, grid_size, num_locations):
    paths = set()
    while len(paths) < num_paths:
        path = tuple(gen_path(grid_size, num_locations))
        paths.add(path)

    return [list(p) for p in paths]

def score_path(path):
    score = 0
    for i in range(1, len(path)):
        distance = math.hypot(path[i-1][0] - path[i][0], path[i-1][1] - path[i][1])
        score += round(distance)
    return score

def score_paths(paths):
    copy_paths = copy.deepcopy(paths)
    optimised_paths = []
    while len(copy_paths) > 0:
        lowest_score = 0
        best_path = 0
        for i in range(0, len(copy_paths)):
            score = score_path(copy_paths[i])
            if lowest_score == 0 or score < lowest_score:
                lowest_score = score
                best_path = i
        optimised_paths.append(copy_paths[best_path])
        copy_paths.pop(best_path)

    return optimised_paths

def add_path_scores(optimised_paths):
    scored_paths = []
    for path in optimised_paths:
        score = score_path(path)
        scored_paths.append((score, path))
    return scored_paths

def print_scored_paths(paths, num_to_print=10):
    for i in range(len(paths)):
        if i == num_to_print:
            break
        print("Score: ", paths[i][0], " for path:\n", paths[i][1])

def crossover(p1, p2):
    p1_len = len(p1)
    c1, c2 = sorted(random.sample(range(p1_len), 2))
    child = [-1] * p1_len

    child[c1:c2] = p1[c1:c2]

    p2_vals = [i for i in p2 if i not in child]
    fill = [i for i in range(p1_len) if child[i] == -1]

    for i, pos in enumerate(fill):
        child[pos] = p2_vals[i]

    return child

def crossover_paths(optimised_paths, decimal_percentage):
    limit = max(2, round((len(optimised_paths) - 1) * decimal_percentage / 2) * 2)
    mutated = set()
    new_children = []

    attempts = 0
    max_attempts = limit * 2

    while len(new_children) < limit and attempts < max_attempts:
        p1, p2 = random.sample(optimised_paths, 2)
        child = tuple(crossover(p1, p2))
        
        if child not in mutated:
            mutated.add(child)
            new_children.append(list(child))
        
        attempts += 1

    while len(new_children) < limit:
        new_children.append(random.choice(optimised_paths))

    return new_children
    
def genetic_algorithm(population, crossover_rate, mutation_rate, generations, tournament_selection_num, counter=0):
    optimised_paths = score_paths(population)

    if counter == generations:
        return optimised_paths
    
    elite = [optimised_paths[0], optimised_paths[1]]
    crossover = crossover_paths(optimised_paths, crossover_rate)

    remaining = generations - len(elite) - len(crossover)
    remaining_pop = tournament_selection(tournament_selection_num, optimised_paths[2:-1], remaining)

    mutated = mutate_paths(elite+crossover+remaining_pop, mutation_rate)
    counter += 1
    return genetic_algorithm(mutated, crossover_rate, mutation_rate, generations, tournament_selection_num, counter)


def tournament_selection(num_selected, paths, limit):
    selected = []
    while len(selected) < limit:
        low = 0
        high = 0
        if (high + num_selected) > len(paths):
            high = len(paths)
        else:
            high += num_selected 
        
        optimised_paths = score_paths(paths[low:high])
        selected.append(optimised_paths[0])
        low = high
    return selected

def mutate(path, mutation_rate):
    n = max(1, round(len(path) * mutation_rate))
    for _ in range(n):
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]

    return path

def mutate_paths(optimised_paths, mutation_rate):
    n = max(1, round(len(optimised_paths) * 0.1))
    to_mutate = random.sample(range(2, len(optimised_paths)), n)
    for i in to_mutate:
        optimised_paths[i] = mutate(optimised_paths[i], mutation_rate)
    return optimised_paths

if __name__ == "__main__":
    main()