from expressions import cross_over, tuple_to_expression
from fitness import evaluate_potential
import math
from random import choices, randint, choice, random
from numpy import argmin
import time
import logging

logging.basicConfig(filename='main.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logging.warning('start running')

# use genetic programming to find the best solution
# initialize population

zs = ('z0', 'z1', 'z2', 'z3', 'z4')
zbs = ('z0b', 'z1b', 'z2b', 'z3b', 'z4b')

J1_z = '(z0*z1*z2*z3*z4)'
J2_z = '(z0**2*z1*z2**2/5 + z0**2*z3**2*z4/5 + z0*z1**2*z4**2/5 + z1**2*z2*z3**2/5 + z2**2*z3*z4**2/5)'
J3_z = '(z0**2*z1**2*z3/5 + z0**2*z2*z4**2/5 + z0*z2**2*z3**2/5 + z1**2*z2**2*z4/5 + z1*z3**2*z4**2/5)'
J4_z = '(z0**3*z1*z4/5 + z0*z1**3*z2/5 + z0*z3*z4**3/5 + z1*z2**3*z3/5 + z2*z3**3*z4/5)'
J5_z = '(z0**3*z2*z3/5 + z0*z1*z3**3/5 + z0*z2**3*z4/5 + z1**3*z3*z4/5 + z1*z2*z4**3/5)'
J6_z = '(z0**5/5 + z1**5/5 + z2**5/5 + z3**5/5 + z4**5/5)'

J1b_z = '(z0b*z1b*z2b*z3b*z4b)'
J2b_z = '(z0b**2*z1b*z2b**2/5 + z0b**2*z3b**2*z4b/5 + z0b*z1b**2*z4b**2/5 + z1b**2*z2b*z3b**2/5 + z2b**2*z3b*z4b**2/5)'
J3b_z = '(z0b**2*z1b**2*z3b/5 + z0b**2*z2b*z4b**2/5 + z0b*z2b**2*z3b**2/5 + z1b**2*z2b**2*z4b/5 + z1b*z3b**2*z4b**2/5)'
J4b_z = '(z0b**3*z1b*z4b/5 + z0b*z1b**3*z2b/5 + z0b*z3b*z4b**3/5 + z1b*z2b**3*z3b/5 + z2b*z3b**3*z4b/5)'
J5b_z = '(z0b**3*z2b*z3b/5 + z0b*z1b*z3b**3/5 + z0b*z2b**3*z4b/5 + z1b**3*z3b*z4b/5 + z1b*z2b*z4b**3/5)'
J6b_z = '(z0b**5/5 + z1b**5/5 + z2b**5/5 + z3b**5/5 + z4b**5/5)'

Js_z = [J1_z, J2_z, J3_z, J4_z, J5_z, J6_z]
Jbs_z = [J1b_z, J2b_z, J3b_z, J4b_z, J5b_z, J6b_z]

J1, J2, J3, J4, J5, J6 = 'J1', 'J2', 'J3', 'J4', 'J5', 'J6'
Js = [J1, J2, J3, J4, J5, J6]
J1b, J2b, J3b, J4b, J5b, J6b = 'J1b', 'J2b', 'J3b', 'J4b', 'J5b', 'J6b'
Jbs = [J1b, J2b, J3b, J4b, J5b, J6b]

population = []

# singletons
population.extend(Js)
population.extend(Jbs)
# integers from 1 to 10 and -1 to -10
# population.extend([i for i in range(1, 11)])
# population.extend([-i for i in range(1, 11)])
# generate random complex constants
for i in range(100):
    # num = randint(1, 10) + 1j * randint(1, 10)
    num = random() * 20 - 10
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
    for i in range(6):  # must replace zbs first, otherwise 'J1b' will be replaced by '(z0*...*z4)b'
        expression = expression.replace(Jbs[i], Jbs_z[i])
    for i in range(6):
        expression = expression.replace(Js[i], Js_z[i])
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
        expr_z = sub_z(expr)
        fitness_value = evaluate_potential(expr_z)  # higher fitness value, less fit
        logging.debug(f'{expr} = {expr_z}: {fitness_value}')
        print(f'{expr}: {fitness_value}')
        if abs(fitness_value) <= 1e-4:
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
