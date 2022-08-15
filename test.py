import torch as t
from torch.autograd import grad
from sympy import *
from random import randint
from timeit import timeit

a = t.tensor(3., requires_grad=True)
b = a ** 2
print(grad(a**2, a, allow_unused=True, create_graph=True, retain_graph=True)[0])

m2 = t.zeros(2, 2)
m2[0, 0] = a
m2[0, 1] = a+2
m2[1, 0] = a
m2[1, 1] = a-3
print(grad(t.det(m2), a, allow_unused=True, create_graph=True)[0])

# m = t.tensor([[a, a], [a, a]], requires_grad=True)
# print(m[0, 0])
#
# s = t.sum(m)
# print(s)
#
# print(grad(s, m[0][0], allow_unused=True, create_graph=True)[0])
#
# print(m.grad)
# s.backward()
# print(m.grad)
# print(a.grad)

# b = a ** 2
#
# for _ in range(5):
#     # print(b.grad_fn)
#     if b.grad_fn is None:
#         t = t.tensor(0)
#     t = grad(b, a, allow_unused=True, create_graph=True)[0]
#     print(t)
#     b = t

# def f(matrix):
#     matrix = matrix.cuda()
#     for i in range(100):
#         matrix += 1
#     return matrix
#
# m = t.tensor([[3, 1], [1, 2]], dtype=t.cfloat)
# print(timeit('f(m)', globals=globals(), number=10000))
#
# fo = t.jit.script(f)
# print(timeit('fo(m)', globals=globals(), number=10000))

# z = Matrix([[-0.4753-1.2322j],
#         [ 0.2786-1.6227j]])
# z_dagger = z.conjugate().transpose()
# m = Matrix([[3, 1], [1, 2]])
#
# print(simplify(z_dagger * m * z))
#
# magnitude = 10
# real_part = t.randint(-magnitude, magnitude + 1, tuple())
# print(real_part)

# m1 = t.tensor([[1.], [5.]])
# m2 = t.tensor([[1., 2.], [3., 1.]])
# m3 = t.transpose(m1, 0, 1)
# print(m3)
# print(m2 * m1)
# print(t.matmul(m2, m1))
# print(t.matmul(m3, t.matmul(m2, m1)))


# print(t.log(t.tensor(2.7139, requires_grad=True)))
# a = t.tensor(2., requires_grad=True)
# b = t.tensor(0., requires_grad=True)
# print(grad(b, a, allow_unused=True, create_graph=True)[0])

# a = t.tensor(2+3j, requires_grad=True)
# b = a * a
# print(grad(b, a)[0])
# print()
#
# a = t.tensor(2+3j, requires_grad=True)
# b = a.conj()
# print(grad(b, a, create_graph=True))
# print(a.grad)
# b.backward()
# print(a.grad)
# print()
#
# a = t.tensor(2+3j, requires_grad=True)
# b = a.conj()
# b.retain_grad()
# b.backward()
# print(a.grad)
#
# d = a * 1 - 1
# a.grad = None
# d.backward()
# print(a.grad)
# print()
#
# a = t.tensor(2 + 3j, requires_grad=True)
# b = a.conj().detach()
# b.requires_grad = True
# c = a * b
# print(a, b, c)
# a.grad = None
# b.grad = None
# c.grad = None
# print(grad(c, a, retain_graph=True))
# print(grad(c, b))
# print(grad(c, c))
# # c.backward()
# # print(a.grad)
# # print(a.grad_fn)
# # print(b.grad)
# # print(c.grad_fn)
#
# # x = t.tensor(2, requires_grad=True)
# # x = x ** 2
#
# print('----------------')
# zs = t.randn(5, dtype=t.cfloat, requires_grad=True)
# z0, z1, z2, z3, z4 = zs
# zbs = zs.conj().detach()
# zbs.requires_grad = True
# z0b, z1b, z2b, z3b, z4b = zbs
# print(zs, zbs)
#
#
# def complex_grad(expr, wrt, zs, zbs):
#     z_type, index = wrt
#     if z_type == 'zs':
#         w = zbs[index]
#     else:
#         w = zs[index]
#     return grad(expr, w, allow_unused=True, retain_graph=True)
#
#
# p = (
#             z0 ** 3 * z1 * z4 / 5 + z0 * z1 ** 3 * z2 / 5 + z0 * z3 * z4 ** 3 / 5 + z1 * z2 ** 3 * z3 / 5 + z2 * z3 ** 3 * z4 / 5) * (
#             z0b ** 2 * z1b * z2b ** 2 / 5 + z0b ** 2 * z3b ** 2 * z4b / 5 + z0b * z1b ** 2 * z4b ** 2 / 5 + z1b ** 2 * z2b * z3b ** 2 / 5 + z2b ** 2 * z3b * z4b ** 2 / 5) * (
#             z0 ** 2 * z1 * z2 ** 2 / 5 + z0 ** 2 * z3 ** 2 * z4 / 5 + z0 * z1 ** 2 * z4 ** 2 / 5 + z0b ** 2 * z1b ** 2 * z3b / 5 + z0b ** 2 * z2b * z4b ** 2 / 5 - z0b * z1b * z2b * z3b * z4b + z0b * z2b ** 2 * z3b ** 2 / 5 + z1 ** 2 * z2 * z3 ** 2 / 5 + z1b ** 2 * z2b ** 2 * z4b / 5 + z1b * z3b ** 2 * z4b ** 2 / 5 + z2 ** 2 * z3 * z4 ** 2 / 5)
# print(p)
#
# n = (2 + 1j) * z0
# print(complex_grad(n, ('zs', 0), zs, zbs))

# x, y, z = symbols('x y z')
# expr = x + y * z
# xt, yt, zt = t.tensor(1.2, requires_grad=True), t.tensor(1.3, requires_grad=True), t.tensor(1.4, requires_grad=True)
#
# res = expr.subs({x: xt, y: yt, z: zt})
# print(res, type(res))
# print(parse_expr("x+1"))
# print(expr.__repr__())
# s = expr.__repr__()
# x, y, z = xt, yt, zt
# print(eval(s))
# r = eval(s)
# print(grad(r, y))
