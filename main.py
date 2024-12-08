import random
import math

#Parameters

target = "Biat a te o pe hai gia' vinto il fantacalcio"
pop_size = 100 #population size
mutation_rate = 0.01
power_base = 4 #bese to get the fitness
max_score = len(target)
max_score_found = False 
ascii_chars = [chr(i) for i in range(32,127)]#all printable ascii chars
generation = 0
T_boltzman = 50


#get a raondom char
def random_char():
    return random.choice(ascii_chars)

#dna class
class DNA(object):
    def __init__(self):
        self.genes = [random_char() for _ in range(len(target))]
        self.score = 0
        self.fitness = 0.0

    def get_str(self):
        return "".join(self.genes)

    def eval_fitness(self):
        global target, max_score, max_score_found
        self.score = sum(1 for idx, value in enumerate(target) if value == self.genes[idx])
        self.fitness = math.pow(power_base, self.score)
        if self.score == max_score:
            max_score_found = True

    def crossover(self, partner):
        child = DNA()
        midpoint = random.randint(0, len(self.genes) - 1)
        child.genes = self.genes[:midpoint] + partner.genes[midpoint:]
        return child

    def mutate(self):
        global mutation_rate
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random_char()


# declaretion of population
population = [DNA() for _ in range(pop_size)]


def roulette_wheel():
    # P(i) = fitness(i)/sum of all fitness
    global population
    fitness_sum = sum(individual.fitness for individual in population)
    pick = random.uniform(0, fitness_sum)
    current = 0
    for individual in population:
        current += individual.fitness
        if current >= pick:
            return individual
    return population[-1]

def softmax(temperature=1.0):
    # P(i) = e^(f(i)/t) / sum of all e^(f(j)/t)

    # t big   -> every one get to fuck
    # t small -> just the fittest get to fuck
    # dinamic apporach -> start by letting fucking everyone to get divesity
    # then start selecting the fittest only
    # t = StartT * (0.99) ^ (generation)

    #to avoid overflow we fint the max
    max_fitness = max(ind.fitness for ind in population)

    #evaluate all the es
    exp_fitness = [math.exp((ind.fitness - max_fitness) / temperature) for ind in population]
    sum_exp_fitness = sum(exp_fitness)
    probabilities = [exp_fit / sum_exp_fitness for exp_fit in exp_fitness]

    pick = random.uniform(0, 1)
    cumulative = 0
    for individual, prob in zip(population, probabilities):
        cumulative += prob
        if pick <= cumulative:
            return individual
    return population[-1]

def step_population():
    global population, T_boltzman, generation
    new_population = []
    for _ in range(pop_size):
        #parent_a = roulette_wheel()
        #parent_b = roulette_wheel()
        current_t = T_boltzman * math.pow(0.99, generation)
        parent_a = softmax(current_t) 
        parent_b = softmax(current_t) 
        child = parent_a.crossover(parent_b)
        child.mutate()
        new_population.append(child)
    population = new_population


def main():
    global generation
    while not max_score_found:
        generation += 1
        for individual in population:
            individual.eval_fitness()

        best_match = max(population, key=lambda x: x.fitness)
        print(f"Generation {generation}: {best_match.get_str()} | Score: {best_match.score}")

        if max_score_found:
            print("\nTarget raggiunto!")
            print(f"Generazione: {generation}")
            print(f"Frase trovata: {best_match.get_str()}")
            break

        step_population()

if __name__ == "__main__":
    main()
