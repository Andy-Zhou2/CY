from sympy import *
from expressions import cross_over, tuple_to_expression
from fitness import evaluate_potential, calculate_test_fitness
import math
from random import choices
from numpy import argmin
import time
import logging

logging.basicConfig(filename='test2.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logging.warning('start running')

# use genetic programming to find the best solution
# initialize population

zs = symbols('z0 z1 z2 z3 z4')
zbs = symbols('z0b z1b z2b z3b z4b')

J1 = prod(zs)
J2 = sum([zs[(i - 1) % 5] ** 2 * zs[i] * zs[(i + 1) % 5] ** 2 for i in range(5)]) / 5
J3 = sum([zs[(i - 2) % 5] ** 2 * zs[i] * zs[(i + 2) % 5] ** 2 for i in range(5)]) / 5
J4 = sum([zs[(i - 1) % 5] * zs[i] ** 3 * zs[(i + 1) % 5] for i in range(5)]) / 5
J5 = sum([zs[(i - 2) % 5] * zs[i] ** 3 * zs[(i + 2) % 5] for i in range(5)]) / 5
J6 = sum([zs[i] ** 5 for i in range(5)]) / 5
# J1b = conjugate(prod(zs))
# J2b = conjugate(sum([zs[(i - 1) % 5] ** 2 * zs[i] * zs[(i + 1) % 5] ** 2 for i in range(5)]) / 5)
# J3b = conjugate(sum([zs[(i - 2) % 5] ** 2 * zs[i] * zs[(i + 2) % 5] ** 2 for i in range(5)]) / 5)
# J4b = conjugate(sum([zs[(i - 1) % 5] * zs[i] ** 3 * zs[(i + 1) % 5] for i in range(5)]) / 5)
# J5b = conjugate(sum([zs[(i - 2) % 5] * zs[i] ** 3 * zs[(i + 2) % 5] for i in range(5)]) / 5)
# J6b = conjugate(sum([zs[i] ** 5 for i in range(5)]) / 5)
J1b = prod(zbs)
J2b = sum([zbs[(i - 1) % 5] ** 2 * zbs[i] * zbs[(i + 1) % 5] ** 2 for i in range(5)]) / 5
J3b = sum([zbs[(i - 2) % 5] ** 2 * zbs[i] * zbs[(i + 2) % 5] ** 2 for i in range(5)]) / 5
J4b = sum([zbs[(i - 1) % 5] * zbs[i] ** 3 * zbs[(i + 1) % 5] for i in range(5)]) / 5
J5b = sum([zbs[(i - 2) % 5] * zbs[i] ** 3 * zbs[(i + 2) % 5] for i in range(5)]) / 5
J6b = sum([zbs[i] ** 5 for i in range(5)]) / 5

Js_z = [J1, J2, J3, J4, J5, J6]
Jbs_z = [J1b, J2b, J3b, J4b, J5b, J6b]

J1, J2, J3, J4, J5, J6 = symbols('J1 J2 J3 J4 J5 J6')
Js = [J1, J2, J3, J4, J5, J6]
J1b, J2b, J3b, J4b, J5b, J6b = symbols('J1b, J2b, J3b, J4b, J5b, J6b')
Jbs = [J1b, J2b, J3b, J4b, J5b, J6b]

population = []

# # singletons
# population.extend(Js)
# population.extend(Jbs)
# # integers from 1 to 10 and -1 to -10
# population.extend([Integer(i) for i in range(1, 11)])
# population.extend([Integer(-i) for i in range(1, 11)])
#
# # forms like z1 * z2
# population.extend([('*', Js[i], Js[j]) for i in range(6) for j in range(6)])
# # forms like z1 * z2b
# population.extend([('*', Js[i], Jbs[j]) for i in range(6) for j in range(6)])
# # forms like z1b * z2b
# population.extend([('*', Jbs[i], Jbs[j]) for i in range(6) for j in range(6)])
#
# # forms like z1 + z2
# population.extend([('+', Js[i], Js[j]) for i in range(6) for j in range(6)])
# # forms like z1 + z2b
# population.extend([('+', Js[i], Jbs[j]) for i in range(6) for j in range(6)])
# # forms like z1b + z2b
# population.extend([('+', Jbs[i], Jbs[j]) for i in range(6) for j in range(6)])
# population.extend(
#     [('*', Js[i], Js[j], Js[k]) for i in range(6) for j in range(6) for k in range(6)])  # Js[i] * Js[j] * Js[k]
# TODO: z1-z2, since we cannot create minus sign out of the air
# TODO: add complex constants

population.extend(zs)
population.extend([Integer(i) for i in range(1, 11)])
population.extend([Integer(-i) for i in range(1, 11)])
population.extend([('+', zs[i], zs[j]) for i in range(5) for j in range(5)])
population.extend([('*', zs[i], zs[j]) for i in range(5) for j in range(5)])
print(population, len(population))


def sub_z(expression):
    for i in range(6):
        expression = expression.subs(Js[i], Js_z[i])
        expression = expression.subs(Jbs[i], Jbs_z[i])
    return expression


epoch = 1
while True:
    logging.info(f'start epoch {epoch}')
    epoch_start_time = time.time()
    fitness_values = []  # used as weights for random selection
    for tuple_expr in population:
        expr = tuple_to_expression(tuple_expr)
        fitness_value = calculate_test_fitness(expr, zs)  # higher fitness value, less fit
        logging.debug(f'{expr}: {fitness_value}')
        if fitness_value == 0:
            logging.info(('found solution', expr))
            import sys

            sys.exit(0)
        fitness_values.append(fitness_value)
    weights = [1 / (v ** 2) for v in fitness_values]

    logging.info(f'average fitness value: {sum(fitness_values) / len(fitness_values)}')
    logging.info(
        f'most fit: {population[argmin(fitness_values)]} = {tuple_to_expression(population[argmin(fitness_values)])}:'
        f'{min(fitness_values)}')

    CROSS_OVER_SIZE = 800
    REPRODUCTION_SIZE = 150

    new_population = []
    for i in range(CROSS_OVER_SIZE):
        parent1 = choices(population, weights=weights, k=1)[0]
        parent2 = choices(population, weights=weights, k=1)[0]
        child = cross_over(parent1, parent2)
        new_population.append(child)
    for i in range(REPRODUCTION_SIZE):
        parent = choices(population, weights=weights, k=1)[0]
        new_population.append(parent)

    new_population_set = set(new_population)

    logging.info((f'next gen of population:', {tuple_to_expression(tuple_expr) for tuple_expr in new_population_set}))
    logging.info(('population size:', len(new_population_set)))

    population = list(new_population_set)
    epoch += 1

    logging.info(f'epoch time: {time.time() - epoch_start_time}')
