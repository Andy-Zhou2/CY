from sympy import *
from random import randint

m = Matrix([[3, 1], [1, 2]])


def generate_random_complex_number():
    real_part = randint(-10, 10)
    imag_part = randint(-10, 10)
    return real_part + imag_part * I


# for _ in range(1000):
#     z = Matrix([[generate_random_complex_number() for _ in range(2)]]).transpose()
#     z_dagger = z.conjugate().transpose()
#     # print(m * z)
#     # print()
#     result = z_dagger * (m * z)
#     # print(result.evalf())
#     # result = result.evalf()
#     # print(result[0])
#     # print(z, z_dagger, simplify(result[0]))
#     assert simplify(result[0]) > 0

print(Integer(1)/Integer(0))
print(oo+1)

print(zoo)