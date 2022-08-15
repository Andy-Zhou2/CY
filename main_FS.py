from sympy import *
from expressions import cross_over, tuple_to_expression
from FB_fitness import evaluate_potential
import math
from random import choices, randint, choice
from numpy import argmin
import time
import logging


logging.basicConfig(filename='FB.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logging.warning('start running')

# use genetic programming to find the best solution
# initialize population

zs = symbols('z0 z1 z2 z3 z4')
zbs = symbols('z0b z1b z2b z3b z4b')

J1_z = prod(zs)
J2_z = sum([zs[(i - 1) % 5] ** 2 * zs[i] * zs[(i + 1) % 5] ** 2 for i in range(5)]) / 5
J3_z = sum([zs[(i - 2) % 5] ** 2 * zs[i] * zs[(i + 2) % 5] ** 2 for i in range(5)]) / 5
J4_z = sum([zs[(i - 1) % 5] * zs[i] ** 3 * zs[(i + 1) % 5] for i in range(5)]) / 5
J5_z = sum([zs[(i - 2) % 5] * zs[i] ** 3 * zs[(i + 2) % 5] for i in range(5)]) / 5
J6_z = sum([zs[i] ** 5 for i in range(5)]) / 5
# J1b = conjugate(prod(zs))
# J2b = conjugate(sum([zs[(i - 1) % 5] ** 2 * zs[i] * zs[(i + 1) % 5] ** 2 for i in range(5)]) / 5)
# J3b = conjugate(sum([zs[(i - 2) % 5] ** 2 * zs[i] * zs[(i + 2) % 5] ** 2 for i in range(5)]) / 5)
# J4b = conjugate(sum([zs[(i - 1) % 5] * zs[i] ** 3 * zs[(i + 1) % 5] for i in range(5)]) / 5)
# J5b = conjugate(sum([zs[(i - 2) % 5] * zs[i] ** 3 * zs[(i + 2) % 5] for i in range(5)]) / 5)
# J6b = conjugate(sum([zs[i] ** 5 for i in range(5)]) / 5)
J1b_z = prod(zbs)
J2b_z = sum([zbs[(i - 1) % 5] ** 2 * zbs[i] * zbs[(i + 1) % 5] ** 2 for i in range(5)]) / 5
J3b_z = sum([zbs[(i - 2) % 5] ** 2 * zbs[i] * zbs[(i + 2) % 5] ** 2 for i in range(5)]) / 5
J4b_z = sum([zbs[(i - 1) % 5] * zbs[i] ** 3 * zbs[(i + 1) % 5] for i in range(5)]) / 5
J5b_z = sum([zbs[(i - 2) % 5] * zbs[i] ** 3 * zbs[(i + 2) % 5] for i in range(5)]) / 5
J6b_z = sum([zbs[i] ** 5 for i in range(5)]) / 5

Js_z = [J1_z, J2_z, J3_z, J4_z, J5_z, J6_z]
Jbs_z = [J1b_z, J2b_z, J3b_z, J4b_z, J5b_z, J6b_z]

J1, J2, J3, J4, J5, J6 = symbols('J1 J2 J3 J4 J5 J6')
Js = [J1, J2, J3, J4, J5, J6]
J1b, J2b, J3b, J4b, J5b, J6b = symbols('J1b, J2b, J3b, J4b, J5b, J6b')
Jbs = [J1b, J2b, J3b, J4b, J5b, J6b]

population = []
# TODO: delete solution
population.append(('+', 1, ('*', zs[0], zbs[0]), ('*', zs[1], zbs[1]), ('*', zs[2], zbs[2]), ('*', zs[3], zbs[3]),
                   ('*', zs[4], zbs[4])))
population.append(('*', ('*', J4, ('+', ('-', J2, J1b), J3b)), J2b))  # TODO: delete

# singletons
population.extend(Js)
population.extend(Jbs)
# integers from 1 to 10 and -1 to -10
population.extend([Integer(i) for i in range(1, 11)])
population.extend([Integer(-i) for i in range(1, 11)])
# generate random complex constants
for i in range(100):
    num = randint(1, 10) + I * randint(1, 10)
    population.append(num)

# forms like z1 * z2
population.extend([('*', Js[i], Js[j]) for i in range(6) for j in range(6)])
# forms like z1 * z2b
population.extend([('*', Js[i], Jbs[j]) for i in range(6) for j in range(6)])
# forms like z1b * z2b
population.extend([('*', Jbs[i], Jbs[j]) for i in range(6) for j in range(6)])

# forms like z1 + z2
population.extend([('+', Js[i], Js[j]) for i in range(6) for j in range(6)])
# forms like z1 + z2b
population.extend([('+', Js[i], Jbs[j]) for i in range(6) for j in range(6)])
# forms like z1b + z2b
population.extend([('+', Jbs[i], Jbs[j]) for i in range(6) for j in range(6)])

# forms like z1 - z2
population.extend([('-', Js[i], Js[j]) for i in range(6) for j in range(6)])
# forms like z1 - z2b
population.extend([('-', Js[i], Jbs[j]) for i in range(6) for j in range(6)])
# forms like z1b - z2b
population.extend([('-', Jbs[i], Jbs[j]) for i in range(6) for j in range(6)])

print(population, len(population))


def sub_z(expression):
    for i in range(6):
        expression = expression.subs(Js[i], Js_z[i])
        expression = expression.subs(Jbs[i], Jbs_z[i])
    return expression


# print('gg:', sub_z(tuple_to_expression(('*', ('*', J4, ('+', ('-', J2, J1b), J3b)), J2b))).__repr__())
def choose_random_formula(population, weights):
    if sum(weights) == 0:
        return choice(population)
    else:
        return choices(population, weights=weights, k=1)[0]


epoch = 1
while True:
    logging.info(f'start epoch {epoch}')
    epoch_start_time = time.time()
    fitness_values = []  # used as weights for random selection
    for tuple_expr in population:
        logging.debug(f'now evaluating: {tuple_expr}')
        expr = tuple_to_expression(tuple_expr)
        expr = sub_z(expr)
        fitness_value = evaluate_potential(expr)  # higher fitness value, less fit
        logging.debug(f'{expr}: {fitness_value}')
        if abs(fitness_value) <= 1:
            logging.info(('found solution', expr))
            import sys

            sys.exit(0)
        fitness_values.append(fitness_value)
    weights = [1 / (v ** 2) for v in fitness_values]

    logging.info(f'average fitness value: {sum(fitness_values) / len(fitness_values)}')
    logging.info(
        f'most fit: {population[argmin(fitness_values)]} = {tuple_to_expression(population[argmin(fitness_values)])}:'
        f'{min(fitness_values)}')

    CROSS_OVER_SIZE = 2000
    REPRODUCTION_SIZE = 400

    new_population = []
    for i in range(CROSS_OVER_SIZE):
        parent1 = choose_random_formula(population, weights)
        parent2 = choose_random_formula(population, weights)
        child = cross_over(parent1, parent2)
        new_population.append(child)
    for i in range(REPRODUCTION_SIZE):
        parent = choose_random_formula(population, weights)
        new_population.append(parent)

    new_population_set = set(new_population)

    logging.info((f'next gen of population:', {tuple_to_expression(tuple_expr) for tuple_expr in new_population_set}))
    logging.info(('population size:', len(new_population_set)))

    population = list(new_population_set)
    epoch += 1

    logging.info(f'epoch time: {time.time() - epoch_start_time}')
