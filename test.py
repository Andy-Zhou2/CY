import torch as t

a = t.tensor(3+1j, dtype=t.complex128)
b = t.tensor(3+1j, dtype=t.cfloat)

print(a, b, b.dtype)
print(a * b)