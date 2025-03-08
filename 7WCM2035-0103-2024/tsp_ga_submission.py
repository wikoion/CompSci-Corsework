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
        copy_paths.pop(i)

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

def mutate_paths(optimised_paths, decimal_percentage):
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
    
def generation(population, mutation_rate, generations, counter=0):
    optimised_paths = score_paths(population)

    if counter == 100:
        return optimised_paths
    
    elite = [optimised_paths[0], optimised_paths[1]]
    mutated = mutate_paths(optimised_paths, mutation_rate)

    remaining = generations - len(elite) - len(mutated)
    remaining_pop = tourname_selection(5, optimised_paths[2:-1], remaining)#
    counter += 1
    return generation(elite+mutated+remaining_pop, mutation_rate, generations, counter)


def tourname_selection(num_selected, paths, limit):
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


locations = gen_paths(100, 100, 10)
optimised_paths = score_paths(locations)
mutated = mutate_paths(optimised_paths, 0.1)
gen = generation(locations, 0.1, 100)
print(len(gen))
