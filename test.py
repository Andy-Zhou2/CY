import torch as t
from torch.autograd import grad

a = t.tensor(3+1j, dtype=t.complex128, requires_grad=True)
b = t.tensor(2+3j, dtype=t.complex128, requires_grad=True)

c = a * b
print(grad(c, a))

nan = t.tensor(float('nan'))
inf = t.tensor(float('inf'))
print(t.isnan(t.tensor([nan, inf])))
print(t.isinf(t.tensor([nan, inf])))

print(bool(t.tensor([True, False])))