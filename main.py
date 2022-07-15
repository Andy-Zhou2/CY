from sympy import *

# use genetic programming to find the best solution
# initialize population

zs = symbols('z0 z1 z2 z3 z4')
print(zs)

J1 = prod(zs)
print(J1)
J2 = sum([zs[(i - 1) % 5] ** 2 * zs[i] * zs[(i + 1) % 5] ** 2 for i in range(5)]) / 5
print(J2)
J3 = sum([zs[(i - 2) % 5] ** 2 * zs[i] * zs[(i + 2) % 5] ** 2 for i in range(5)]) / 5
print(J3)
J4 = sum([zs[(i - 1) % 5] * zs[i] ** 3 * zs[(i + 1) % 5] for i in range(5)]) / 5
print(J4)
J5 = sum([zs[(i - 2) % 5] * zs[i] ** 3 * zs[(i + 2) % 5] for i in range(5)]) / 5
print(J5)
J6 = sum([zs[i] ** 5 for i in range(5)]) / 5
print(J6)

Js_z = [J1, J2, J3, J4, J5, J6]
print(Js_z)

J1, J2, J3, J4, J5, J6 = symbols('J1 J2 J3 J4 J5 J6')
Js = [J1, J2, J3, J4, J5, J6]

population = []
population.extend(Js)
population.extend([Integer(i) for i in range(1, 11)])
population.extend([Integer(-i) for i in range(1, 11)])
population.extend([Js[i] * Js[j] for i in range(6) for j in range(6)])
population.extend([Js[i] + Js[j] for i in range(6) for j in range(6)])
population.extend([Js[i] * Js[j] * Js[k] for i in range(6) for j in range(6) for k in range(6)])
print(population, len(population))

expr = population[-1]
print(expr)


def sub_z(expression):
    for i in range(6):
        expression = expression.subs(Js[i], Js_z[i])
    return expression


print(sub_z(expr))
expr = J1 + J2
print(expr.is_Mul)
print(expr.is_Add)
print(expr.is_Pow)
print(expr.args)

print(sub_z(expr).args)
print(diff(sub_z(expr), zs[0]))
