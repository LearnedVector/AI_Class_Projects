# Michael Nguyen 2017
# Need python 3.6 to run
# Genetic Algorithm to solve the N queens problem
#   Algorithm
#   1. Generate the Population
#   2. Determine Fitness
#   3. Run Genetic Algorithm
#       a. Select Parents
#       b. Crossover/Reproduction
#           i. Maybe Mutate
#       c. Loops back to a if fitness != 0

import random
import operator


class NQueensPosition:
    """
    Holds the attributes of each board position
    """
    def __init__(self):
        self.sequence = None
        self.fitness = None

    def setSequence(self, val):
        self.sequence = val

    def setFitness(self, fitness):
        self.fitness = fitness

    def getAttr(self):
        return {'sequence': self.sequence,
                'fitness': self.fitness}


def reportFitness(population):
    """
    Reports the average, best and worse fitness in the
    current generation popultion pool
    """
    sum_of_fitness = 0
    best = 100
    worse = 0
    for i in range(len(population)):
        fitness = population[i].fitness
        sum_of_fitness = + population[i].fitness
        if fitness < best:
            best = fitness
        if fitness > worse:
            worse = fitness

    average = (best + worse)/2
    return average, best, worse


def fitness(N, sequence=None):
    """
    Calculates the fitness by looking for conflicts for row, columns, and diagnols
    """
    conflicts = 0

    # row and column conflicts
    row_and_col = abs(len(sequence) - len(set(sequence)))
    conflicts = + row_and_col
    # calculate diagonal conflicts
    for i in range(len(sequence)):
        for j in range(len(sequence)):
            if (i != j):
                dx = abs(i-j)
                dy = abs(sequence[i] - sequence[j])
                if(dx == dy):
                    conflicts += 1

    return conflicts


def generatePositions(N):
    """
    Generates the poisitions for each column between 0 and N
    """
    position = [i for i in range(N)]
    random.shuffle(position)
    return position


def generatePopulation(N, population_size=200):
    """
    Generates the initial population pool
    """
    population = [NQueensPosition() for i in range(population_size)]

    for i in range(population_size):
        population[i].setSequence(generatePositions(N))
        population[i].setFitness(fitness(N, population[i].sequence))
    return population


def mutate(child):
    """
    Mutate if the random number generate is less then the mutation value
    It iterates through the columns and maybe mutate it
    """
    for i in child.sequence:
        if random.random() < mutation:
            n = len(child.sequence)
            child.sequence[i] = random.randint(0, n-1)
    return child


def reproduction(parent_one, parent_two):
    """
    Crossover function to create the child. Common positions of both parents transfer to child. 
    If a position is not common then a position is picked randomly from parent 1 or 2
    """
    n = len(parent_one.sequence)
    child = NQueensPosition()
    child_sequence = [i for i in range(len(parent_one.sequence))]
    for i in range(len(parent_one.sequence)):
        if parent_one.sequence[i] == parent_two.sequence[i]:
            child_sequence[i] = parent_one.sequence[i]
        else:
            choices = [parent_one.sequence[i], parent_two.sequence[i]]
            child_sequence[i] = random.choice(choices)

    child.setSequence(child_sequence)
    child.setFitness(fitness(n, child_sequence))
    maybe_mutate_child = mutate(child)
    return maybe_mutate_child


def selectParents(population):
    """
    only the fittest 1/10 of the population goes into the selection pool.
    Then the parents are selected by random
    """
    best_parents = population[:int(len(population)/10)]
    parent_one = random.choice(best_parents)
    parent_two = random.choice(best_parents)

    return parent_one, parent_two


def sortByFitness(population):
    """
    Sort's population by lowest fitness first
    """
    population.sort(key=operator.attrgetter('fitness'))
    return population


def geneticAlgorithm(population):
    """
    Main algorithm that takes in initial population and runs the Genetic Algorithm.
        1. Select parents
        2. Create a new population of children
        3. Loops back to 1 if new children population does not contain a 0 fitness
    """
    solution = None
    generation = 1
    if population[0] == 0:
        solution = new_population[0]

    else:
        condition = True
        new_population = population

        while condition:
            sorted_population = sortByFitness(new_population)
            parent_one, parent_two = selectParents(sorted_population)
            child_population = []

            for i in range(len(population)):
                child = reproduction(parent_one, parent_two)
                child_population.append(child)

            sorted_child = sortByFitness(child_population)

            if sorted_child[0].fitness == 0:
                solution = sorted_child[0]
                average, best, worse = reportFitness(sorted_child)
                print("generation", generation, "average", average, "best", best, "worse", worse)
                print(solution.getAttr())
                generation += 1
                condition = False
            else:
                new_population = sorted_child
                average, best, worse = reportFitness(sorted_child)
                print("generation", generation, "average", average, "best", best, "worse", worse)
                # print(sorted_child[0].getAttr())
                generation += 1

    return solution

if __name__ == '__main__':
    N = 0
    while N <= 3 or N >= 10:
        print("Please enter a value between 4 and 10")
        N = int(input("N: "))

    mutation = 0.01
    population = generatePopulation(N, 200)
    sort_population = sortByFitness(population)
    average, best, worse = reportFitness(population)
    solution = geneticAlgorithm(population)
