import pickle as pickle
from sympy import *

if __name__ == '__main__':
    from random import random

    NUM_SAMPLES = 100

    data_points = []
    for _ in range(NUM_SAMPLES):
        point = []
        for _ in range(5):
            # generate random real numbers between -100 and 100
            real = random() * 200 - 100
            imag = random() * 200 - 100
            point.append(real + imag * I)

        z0, z1, z2, z3, z4 = point
        expression = simplify(z0 * 2 + z1 * z4 + z2 * 4 + z3 * z4 + z4 * 6)
        point.append(expression)
        data_points.append(point)

        print(point)
    with open('test_data_points2.pkl', 'wb') as f:
        pickle.dump(data_points, f)


def read_test_data():
    with open('test_data_points2.pkl', 'rb') as f:
        data_points = pickle.load(f)
    return data_points[:20]
