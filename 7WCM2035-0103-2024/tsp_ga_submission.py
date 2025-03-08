import random
import math
import copy

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
    paths = []
    for i in range(1, num_paths):
        paths.append(gen_path(grid_size, num_locations))
    return paths

def score_path(path):
    score = 0
    for i in range(1, len(path)-1):
        distance = math.hypot(path[i-1][0] - path[i][0], path[i-1][1] - path[i][1])
        score += round(distance)
    return score

def score_paths(paths):
    copy_paths = copy.deepcopy(paths)
    optimised_paths = []
    while len(copy_paths) > 0:
        lowest_score = 0
        best_path = 0
        for i in range(0, len(copy_paths)-1):
            score = score_path(copy_paths[i])
            if lowest_score == 0 or score < lowest_score:
                lowest_score = score
                best_path = i
        optimised_paths.append(copy_paths[best_path])
        copy_paths.pop(best_path)

    return optimised_paths

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
    mutated = []

    for i in range(0, limit-1):
        p1 = optimised_paths[i]
        p2 = optimised_paths[i+1]

        mutated.append(crossover(p1, p2))
    return mutated

def genetic_algorithm(num_paths=100, num_locations=10, grid_size=100, mutation_rate=0.1, generations=100):
    cities = gen_paths(num_paths, grid_size, num_locations)

    counter = 0
    
def generation(population, crossover_rate, generations, counter=0):
    optimised_paths = score_paths(population)

    if counter == 100:
        return optimised_paths
    
    elite = [optimised_paths[0], optimised_paths[1]]
    crossover = crossover_paths(optimised_paths, crossover_rate)

    remaining = generations - len(elite) - len(crossover)
    remaining_pop = tournament_selection(5, optimised_paths[2:-1], remaining)

    mutated = mutate_paths(elite+crossover+remaining_pop)
    counter += 1
    return generation(mutated, crossover_rate, generations, counter)


def tournament_selection(num_selected, paths, limit):
    selected = []
    while len(selected) < limit:
        low = 0
        high = 0
        if (high + num_selected) > len(paths)-1:
            high = len(paths)-1
        else:
            high += num_selected 
        
        optimised_paths = score_paths(paths[low:high])
        selected.append(optimised_paths[0])
        low = high
    return selected

def mutate(path, mutation_rate=0.05):
    n = max(1, round(len(path) * mutation_rate))
    for _ in range(n):
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]

    return path

def mutate_paths(optimised_paths, mutation_rate=0.05):
    n = max(1, round(len(optimised_paths) * 0.1))
    to_mutate = random.sample(range(2, len(optimised_paths)), n)
    for i in to_mutate:
        optimised_paths[i] = mutate(optimised_paths[i], mutation_rate)
    return optimised_paths

locations = gen_paths(100, 100, 10)
optimised_paths = score_paths(locations)
gen = generation(locations, 0.1, 100)
print(len(gen))
