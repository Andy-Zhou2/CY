from sympy import *
from random import randint
import math

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

print(oo)
print(abs(1+I*2))
print(2161299**2)

from expressions import tuple_to_expression
zs = symbols('z0 z1 z2 z3 z4')
z0, z1, z2, z3, z4 = zs
print(tuple_to_expression(
    ('+', ('+', ('+', z4, 4), 4), ('+', ('+', z2, ('+', z0, ('+', ('+', 4, ('+', z3, ('*', ('+', z3, ('+', z1, 4)), z4))), z2))), z2))
))

expr = (-98.2622917094188 - 37.8335262783666*I)*(-51.5690226136447 - 19.3633749484099*I + (-98.2622917094188 - 37.8335262783666*I)*(-51.5690226136447 - 19.3633749484099*I)) + (-48.7420807843228 - 24.1075832731616*I)*(77.7726843033887 - 80.9046977685153*I)
print(expr)
print(simplify(expr))
print(abs(expr))
print(simplify(abs(expr)))
print(simplify(abs(simplify(expr))))