import random

def fitness_function(schedule):
    return sum([int(slot) for slot in schedule])

def generate_population(size, gene_length):
    return [''.join(random.choice('01') for _ in range(gene_length)) for _ in range(size)]

# Select parents using roulette wheel selection
def roulette_wheel_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for i, fitness in enumerate(fitnesses):
        current += fitness
        if current > pick:
            return population[i]

def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    return parent1, parent2

# Perform mutation (flip random bits)
def mutate(schedule, mutation_rate):
    schedule = list(schedule)
    for i in range(len(schedule)):
        if random.random() < mutation_rate:
            schedule[i] = '1' if schedule[i] == '0' else '0'
    return ''.join(schedule)

# Main GA process
def genetic_algorithm(pop_size, gene_length, generations, crossover_rate, mutation_rate):
    population = generate_population(pop_size, gene_length)
    best_overall = None

    for generation in range(generations):
        # Evaluate fitness
        fitnesses = [fitness_function(schedule) for schedule in population]
        best_in_generation = max(zip(population, fitnesses), key=lambda x: x[1])
        
        # Track the overall best soluti
        if best_overall is None or best_in_generation[1] > best_overall[1]:
            best_overall = best_in_generation

        # Log current generation
        print(f"Generation {generation + 1}:")
        print(f"Population: {population}")
        print(f"Fitnesses: {fitnesses}")
        print(f"Best in Generation: Schedule {best_in_generation[0]} with Fitness: {best_in_generation[1]}")
        print()

        new_population = [best_in_generation[0]]

        while len(new_population) < pop_size:
            parent1 = roulette_wheel_selection(population, fitnesses)
            parent2 = roulette_wheel_selection(population, fitnesses)
            offspring1, offspring2 = crossover(parent1, parent2, crossover_rate)
            new_population.extend([mutate(offspring1, mutation_rate), mutate(offspring2, mutation_rate)])

        population = new_population[:pop_size]

    print(f"Final Best Solution: Schedule {best_overall[0]}, Fitness: {best_overall[1]}")

genetic_algorithm(pop_size=10, gene_length=24, generations=10, crossover_rate=0.9, mutation_rate=0.5)