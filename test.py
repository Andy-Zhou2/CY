from sympy import *
from random import randint
import math

x = symbols('x')
print(x)
print(type(x-x))
a = x - x
print(a.subs(x, 5))