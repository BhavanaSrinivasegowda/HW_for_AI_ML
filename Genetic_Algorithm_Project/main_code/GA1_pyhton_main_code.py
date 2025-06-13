import numpy as np
import datetime
import tracemalloc
import time
import cProfile

def create_gen(panjang_target):
    random_number = np.random.randint(32, 126, size=panjang_target)
    gen = ''.join([chr(i) for i in random_number])
    return gen

def calculate_fitness(gen, target, panjang_target):
    fitness = 0
    for i in range(panjang_target):
        if gen[i:i + 1] == target[i:i + 1]:
            fitness += 1
    fitness = fitness / panjang_target * 100
    return fitness

def create_population(target, max_population, panjang_target):
    populasi = {}
    for _ in range(max_population):
        gen = create_gen(panjang_target)
        genfitness = calculate_fitness(gen, target, panjang_target)
        populasi[gen] = genfitness
    return populasi

def selection(populasi):
    pop = dict(populasi)
    parent = {}
    for i in range(2):
        gen = max(pop, key=pop.get)
        parent[gen] = pop[gen]
        if i == 0:
            del pop[gen]
    return parent

def crossover(parent, target, panjang_target):
    child = {}
    cp = round(len(list(parent)[0]) / 2)
    for i in range(2):
        gen = list(parent)[i][:cp] + list(parent)[1 - i][cp:]
        genfitness = calculate_fitness(gen, target, panjang_target)
        child[gen] = genfitness
    return child

def mutation(child, target, mutation_rate, panjang_target):
    mutant = {}
    for i in range(len(child)):
        data = list(list(child)[i])
        for j in range(len(data)):
            if np.random.rand(1) <= mutation_rate:
                data[j] = chr(np.random.randint(32, 126))
        gen = ''.join(data)
        genfitness = calculate_fitness(gen, target, panjang_target)
        mutant[gen] = genfitness
    return mutant

def regeneration(mutant, populasi):
    for _ in range(len(mutant)):
        bad_gen = min(populasi, key=populasi.get)
        del populasi[bad_gen]
    populasi.update(mutant)
    return populasi

def bestgen(parent):
    return max(parent, key=parent.get)

def bestfitness(parent):
    return parent[max(parent, key=parent.get)]

def display(parent, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print(f"{bestgen(parent)}\t{round(bestfitness(parent), 2)}%\t{timeDiff}")

# -------------------------------------------
# Main Function with Benchmarking + cProfile
# -------------------------------------------
def main():
    # Start benchmarking
    start_benchmark_time = time.time()
    tracemalloc.start()

    # Parameters
    target = 'Hello World!'
    max_population = 10
    mutation_rate = 0.2
    panjang_target = len(target)

    print('Target Word :', target)
    print('Max Population :', max_population)
    print('Mutation Rate :', mutation_rate)
    print('----------------------------------------------')
    print('The Best\tFitness\tTime')
    print('----------------------------------------------')

    startTime = datetime.datetime.now()
    populasi = create_population(target, max_population, panjang_target)
    parent = selection(populasi)
    display(parent, startTime)

    while True:
        child = crossover(parent, target, panjang_target)
        mutant = mutation(child, target, mutation_rate, panjang_target)
        if bestfitness(parent) >= bestfitness(mutant):
            continue
        populasi = regeneration(mutant, populasi)
        parent = selection(populasi)
        display(parent, startTime)
        if bestfitness(mutant) >= 100:
            break

    # End benchmarking
    end_benchmark_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n=========== Benchmarking Summary ===========")
    print(f"Execution Time: {end_benchmark_time - start_benchmark_time:.4f} seconds")
    print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
    print("============================================")

# Run with cProfile
if __name__ == "__main__":
    cProfile.run('main()', sort='time')
