import torch as t
from torch.autograd import grad
import timeit
from random import randint, choices
import logging

points = []
with open('points_on_quintic.txt', 'r') as data_file:
    lines = data_file.readlines()

for line in lines:
    if line[-1] == '\n':
        line = line[:-1]
    points.append([float(num) for num in line.split('\t')])

points = choices(points, k=30)

BAD_EXPR_FITNESS = 999


def is_positive_definite(matrix, samples=1000):
    """check if a 5x5 matrix is positive definite"""

    def generate_random_complex_number_int_component(magnitude=20):
        while True:
            real_part = randint(-magnitude, magnitude + 1)
            imag_part = randint(-magnitude, magnitude + 1)
            if real_part != 0 or imag_part != 0:
                break
        return t.tensor(real_part + imag_part * 1j, dtype=t.cfloat)

    for _ in range(samples):
        z = t.tensor([[generate_random_complex_number_int_component() for _ in range(5)]]).transpose(0, 1)
        z_dagger = t.transpose(t.conj(z), 0, 1)
        result = t.matmul(z_dagger, t.matmul(matrix, z))[0][0]
        # print('res, z, zd, m:', result, z, z_dagger, matrix, sep='\n', end='\n\n')
        if result.imag > 1e-3 or result.real <= 1e-4:
            return False
    return True


def complex_differentiate(value, wrt):
    """
    Differentiate a complex valued function.
    """
    if value.grad_fn is None:  # usually happens when we get a 0
        return t.tensor(0.)

    result = grad(value, wrt, allow_unused=True, create_graph=True)[0]
    if result is None:  # wrt is unused
        return t.tensor(0.)
    else:
        return result

def check_hermitian(matrix):
    for i in range(5):
        for j in range(i + 1, 5):
            if abs(matrix[i][j] - matrix[j][i].conj()) > 1e-4:
                return False
    for i in range(5):
        if abs(matrix[i][i].imag) > 1e-4:
            return False
    return True

def correct_hermitian(matrix):
    """Take average of matrix and its conjugate transpose. Take real part along diagonal."""
    result = t.zeros(5, 5, dtype=t.cfloat)
    for i in range(5):
        for j in range(i + 1, 5):
            result[i][j] = (matrix[i][j] + matrix[j][i].conj()) / 2
            result[j][i] = result[i][j].conj()
    for i in range(5):
        result[i][i] = matrix[i][i].real
    return result


def evaluate_potential(potential):
    logging.debug('potential: %s', potential)
    err_total = 0.

    for point_index in range(len(points)):
        point = points[point_index]
        logging.debug(('now sub point:', point))
        k = 1e-2
        z0 = t.tensor(k * 1., requires_grad=True)
        z1 = t.tensor(k * (point[0] + 1j * point[1]), requires_grad=True)
        z2 = t.tensor(k * (point[2] + 1j * point[3]), requires_grad=True)
        z3 = t.tensor(k * (point[4] + 1j * point[5]), requires_grad=True)
        z4 = t.tensor(k * (point[6] + 1j * point[7]), requires_grad=True)
        zs = [z0, z1, z2, z3, z4]

        z0b = z0.conj().detach().requires_grad_(True)
        z1b = z1.conj().detach().requires_grad_(True)
        z2b = z2.conj().detach().requires_grad_(True)
        z3b = z3.conj().detach().requires_grad_(True)
        z4b = z4.conj().detach().requires_grad_(True)
        zbs = [z0b, z1b, z2b, z3b, z4b]

        logging.debug(('zs:', zs, 'zbs:', zbs))

        # calculate potential
        p = eval(potential)
        logging.debug(('p:', p))
        if not isinstance(p, t.Tensor):  # if not a tensor, it's a constant
            return BAD_EXPR_FITNESS

        # check if potential is real
        if p.imag.abs().max() > 1e-4:
            logging.debug(('Not real. point, img part, potential:', point, p.imag, p))
            return BAD_EXPR_FITNESS

        # calculate metric g
        g = t.zeros(5, 5, dtype=t.cfloat)
        for i in range(5):
            temp = complex_differentiate(p, zs[i])
            logging.debug(('g_entry i, temp:', i, temp))
            for j in range(5):
                entry = complex_differentiate(temp, zbs[j])
                logging.debug(('g_entry', i, j, entry))
                g[i][j] = entry

        logging.debug(('g:', g))

        # check if g is hermitian
        if not check_hermitian(g):
            logging.debug(('Not hermitian. point, g:', point, g))
            return BAD_EXPR_FITNESS

        # make g perfectly Hermitian
        g = correct_hermitian(g)

        # check if g is positive definite
        if not is_positive_definite(g):
            logging.debug(('not positive definite. point, g:', point, g))
            return BAD_EXPR_FITNESS

        # calculate R and sum to get err
        det = t.det(g)
        ln_det_g = t.log(det)
        logging.debug(('ln_det_g:', ln_det_g, 'det:', det))

        for i in range(5):
            temp = complex_differentiate(ln_det_g, zs[i])
            logging.debug(('R entry i, temp:', i, temp))
            for j in range(5):
                entry = complex_differentiate(temp, zbs[j])
                logging.debug(('R entry:', i, j, entry))
                err_total += entry.detach().item()

    logging.debug(('err_total:', err_total))
    err_total = abs(err_total)
    print('someone survived!', potential, err_total)
    return err_total
