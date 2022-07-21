import pickle as pickle

if __name__ == '__main__':
    from random import random

    NUM_SAMPLES = 1000

    data_points = []
    for _ in range(NUM_SAMPLES):
        point = []
        # generate random real numbers between -100 and 100
        # total of 10 numbers generated
        for _ in range(10):
            point.append(random() * 200 - 100)
        sum_real = sum(point[::2])
        sum_imag = sum(point[1::2])
        point.append(sum_real)
        point.append(sum_imag)
        data_points.append(point)

    with open('test_data_points.pkl', 'wb') as f:
        pickle.dump(data_points, f)


def read_test_data():
    with open('test_data_points.pkl', 'rb') as f:
        data_points = pickle.load(f)
    return data_points[:50]
