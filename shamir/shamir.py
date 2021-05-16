import random
from random import randint
from sys import maxsize
from typing import List, Tuple

from sympy import isprime

P_MAX = maxsize
N = 6
K = 4
M = 123


def rand_prime(min, max):
    x = randint(min, max)
    while not isprime(x):
        x = randint(min, max)
    return x


def f(aa: List[int], x: int, p: int) -> int:
    return sum([a * pow(x, i) for i, a in enumerate(aa)]) % p


# ax + by = gcd
# gcd, x, y = extended_gcd(a, b)
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_gcd(b % a, a)

    x: int = y1 - (b // a) * x1
    y: int = x1

    return gcd, x, y


# k = 3
# a_2 * x ^ 2 + a_1 * x + a_0
# по трем точкам
# (x1, y1), (x2, y2), (x3, y3)
# l_1(x) = (x - x2) * (x - x3) / ((x1 - x2) * (x1 - x3)) =
# = (x ^ 2 - (x2 + x3) * x + x2 * x3) / ((x1 - x2) * (x1 - x3))
# из этого всего нам нужен только x2 * x3 / ((x1 - x2) * (x1 - x3)) для вычисления a_0
#
# эта функция считает этот последний член
# [для параболы: x2 * x3 / ((x1 - x2) * (x1 - x3))]
def l_i_0(xs: List[int], i: int, p: int) -> int:
    dividend = 1
    divisor = 1
    x_i = xs[i]

    for j, x in enumerate(xs):
        if j == i:
            continue

        x_j = xs[j]
        dividend *= -x_j
        divisor *= (x_i - x_j)

    dividend %= p
    divisor %= p

    # dividend / divisor mod p <=> dividend * divisor_inv mod p
    # a * a_inv = 1

    # ax + by = gcd
    gcd, x, y = extended_gcd(divisor, p)
    assert gcd == 1
    divisor_inv = x

    return (dividend * divisor_inv) % p


if __name__ == '__main__':
    print(f'The original secret is: {M}')

    p = rand_prime(M + 1, P_MAX)
    print(f'Let p: {p}')

    aa = [randint(1, p - 1) for i in range(0, K - 1)]
    aa = [M] + aa
    print(f'Let polynom coefficients be: {aa}')

    parts: List[Tuple[int, int]] = [(i + 1, f(aa, i + 1, p)) for i in range(0, N)]
    print(f'Split secret into {N} parts: {parts}')

    sample: List[Tuple[int, int]] = random.sample(parts, k=K)
    print(f'Taking {K} random parts to recreate secret: {sample}')

    xs = [x for x, y in sample]
    ys = [y for x, y in sample]

    recreated_secret = sum([y * l_i_0(xs, i, p) for i, y in enumerate(ys)]) % p
    print(f'Recreated secret: {recreated_secret}')
