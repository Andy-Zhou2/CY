from numba import jit, njit
import random
import time


@jit
def monte_carlo_pi(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

start_time = time.time()
print(monte_carlo_pi(1000000000))
print('time:', time.time() - start_time)