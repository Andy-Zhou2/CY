from sympy import *
from expressions import cross_over, tuple_to_expression
from fitness import evaluate_potential

# use genetic programming to find the best solution
# initialize population

zs = symbols('z0 z1 z2 z3 z4')
zbs = symbols('z0b z1b z2b z3b z4b')
print(zs)

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
print(Js_z, Jbs_z)

J1, J2, J3, J4, J5, J6 = symbols('J1 J2 J3 J4 J5 J6')
Js = [J1, J2, J3, J4, J5, J6]
J1b, J2b, J3b, J4b, J5b, J6b = symbols('J1b, J2b, J3b, J4b, J5b, J6b')
Jbs = [J1b, J2b, J3b, J4b, J5b, J6b]

population = []

# singletons
population.extend(Js)
population.extend(Jbs)
# integers from 1 to 10 and -1 to -10
population.extend([Integer(i) for i in range(1, 11)])
population.extend([Integer(-i) for i in range(1, 11)])

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
population.extend(
    [('*', Js[i], Js[j], Js[k]) for i in range(6) for j in range(6) for k in range(6)])  # Js[i] * Js[j] * Js[k]
print(population, len(population))

expr = 1 + sum(zs[i]*zbs[i] for i in range(5))
print(expr)


def sub_z(expression):
    for i in range(6):
        expression = expression.subs(Js[i], Js_z[i])
    return expression


expr = tuple_to_expression(expr)
print('tuple to expr:', expr)
print(sub_z(expr))
expr = sub_z(expr)
# expr = J1 + J2
#
# print(sub_z(expr).args)
# print(diff(sub_z(expr), zs[0]))

print(evaluate_potential(expr, zs, zbs))

