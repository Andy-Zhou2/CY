from sympy import *
from random import randint, choices


# class Node:
#     def __init__(self, type, children=None):
#         self.type = type
#         self.children = children or []
#
#     def to_expression(self):
#         raise NotImplementedError
#
# class Addition(Node):
#     def to_expression(self):
#         return sum(child.to_expression() for child in self.children)
#
# class Multiplication(Node):
#     def to_expression(self):
#         return prod(child.to_expression() for child in self.children)
#
# class TreeExpression:
#     ...

# example expression: x, ('+', ('*', 'x', 'y'), ('*', 'x', 'z')): x * y + x * z
def count_nodes(expr):
    if isinstance(expr, tuple):
        return 1 + sum(count_nodes(child) for child in expr)
    else:
        return 1


def get_random_subtree(expr):
    if isinstance(expr, tuple):
        weights = [count_nodes(child) for child in expr[1:]]
        if randint(0, sum(weights)) == 0:
            return expr
        else:
            return get_random_subtree(choices(expr[1:], weights=weights, k=1)[0])
    else:
        return expr


print(get_random_subtree(('+', ('*', 'x', 'y'), ('*', 'x', 'z'))))


# ('+', ('*', 'x', 'y'), ('*', 'x', 'z'))

def random_sub(expr, replacement):
    if isinstance(expr, tuple):
        weights = [count_nodes(child) for child in expr[1:]]
        if randint(0, sum(weights)) == 0:
            return replacement
        else:
            replace_node_num = choices(range(1, len(expr)), weights=weights, k=1)[0]
            return expr[:replace_node_num] + (random_sub(expr[replace_node_num], replacement),) + expr[
                                                                                                  replace_node_num + 1:]
    else:
        return replacement


def cross_over(expr1, expr2):
    if randint(0, 1) == 0:
        return random_sub(expr1, get_random_subtree(expr2))
    else:
        return random_sub(expr2, get_random_subtree(expr1))

def tuple_to_expression(expr): # TODO: change into sympy expression (currently has priority issues)
    if isinstance(expr, tuple):
        if expr[0] == '+':
            return '(' + '+'.join([tuple_to_expression(e) for e in expr[1:]]) + ')' #sum(tuple_to_expression(child) for child in expr[1:])
        elif expr[0] == '*':
            return '(' + '*'.join([tuple_to_expression(e) for e in expr[1:]]) + ')' #prod(tuple_to_expression(child) for child in expr[1:])
    else:
        return expr

for i in range(100):
    ex = cross_over(('+', ('*', 'x', 'y'), ('*', 'x', 'z')), ('+', 't', 'a', 'b'))
    print(ex)
    print(tuple_to_expression(ex))
