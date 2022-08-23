from sympy import *
from time import time
from random import randint
import logging

points = []
with open('points_on_quintic.txt', 'r') as data_file:
    lines = data_file.readlines()

for line in lines:
    if line[-1] == '\n':
        line = line[:-1]
    points.append([float(num) for num in line.split('\t')])

points = points[:3000]  # could consider choosing more points
# print('number of sampled points:', len(points))
points.insert(0, (0.1, 0, 0.2, 0, 0.3, 0, 0.4, 0))
# for line in points:
#     assert len(line) == 8
#     for num in line:
#         assert isinstance(num, float)


def generate_random_complex_number(magnitude=10):
    while True:
        real_part = randint(-magnitude, magnitude + 1)
        imag_part = randint(-magnitude, magnitude + 1)
        if real_part != 0 or imag_part != 0:
            break
    return real_part + imag_part * I


def is_positive_definite(matrix, samples=100):
    """check if a 5x5 matrix is positive definite"""
    for _ in range(samples):
        z = Matrix([[generate_random_complex_number() for _ in range(5)]]).transpose()
        z_dagger = z.conjugate().transpose()
        result = z_dagger * (matrix * z)
        if simplify(result[0]) <= 0:
            return False
    return True


def evaluate_potential(potential, zs, zbs):
    """expression should not be in tuple form"""
    potential = ln(potential)
    g = []  # should be a 5x5 matrix
    for i in range(5):
        g.append([])
        for j in range(5):
            g[i].append(diff(diff(potential, zs[i]), zbs[j]))

    g = Matrix(g)
    g_det = g.det()
    logging.debug(('potential:', potential, 'g:', g, 'det:', g_det))

    temp_expr = ln(g_det)

    tensor_expressions = []
    for i in range(5):
        tensor_expressions.append([])
        for j in range(5):
            tensor_expressions[i].append(diff(diff(temp_expr, zs[i]), zbs[j]))
            logging.debug(('tensor_expressions:', tensor_expressions))

    error_total = 0
    start_time = time()
    for point in points:
        z0 = 1
        z1 = point[0] + I * point[1]
        z2 = point[2] + I * point[3]
        z3 = point[4] + I * point[5]
        z4 = point[6] + I * point[7]
        zs_concrete = [z0, z1, z2, z3, z4]
        zbs_concrete = [conjugate(z) for z in zs_concrete]

        concrete_expressions = []
        for i in range(5):
            concrete_expressions.append([])
            for j in range(5):
                err = tensor_expressions[i][j].subs(zs[i], zs_concrete[i])
                err = err.subs(zbs[j], zbs_concrete[j])
                concrete_expressions[i].append(err)

                if is_positive_definite(Matrix(tensor_expressions)):
                    error_total += abs(concrete_expressions[i][j])
                else:
                    logging.debug((potential, 'not positive definite'))
                    return oo
    logging.debug((potential, 'points substitution time:', time() - start_time))
    return error_total
