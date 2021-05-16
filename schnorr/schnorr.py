from random import randint

from sympy import isprime


def rand_prime(min, max):
    x = randint(min, max)
    while not isprime(x):
        x = randint(min, max)
    return x


#### I параметры домена

Q = rand_prime(2 ** 8, 2 ** 15)
print(f'Q={Q}')

TWO_POW = 2 ** 51
c = 0
P = Q * TWO_POW + 1
while not isprime(P):
    c += 1
    P = Q * (TWO_POW + c) + 1
print(f'P={P}')

assert isprime(Q)
assert isprime(P)
assert (P - 1) % Q == 0

G = 1
while G == 1:
    H = randint(2, P)
    q = (P - 1) // Q
    G = pow(H, q, P)
print(f'G={G}')

#### II Y - открытый ключ автора

x = randint(1, Q - 1)
Y = pow(G, x, P)
print(f'x={x}, Y={Y}')

#### III подпись сообщения

M = 'He visited this country also with a view'

k = randint(1, Q - 1)
R = pow(G, k, P)
print(f'R={R}')
E = abs(hash(f'{M}{R}'))
S = (k - x * E) % Q
print(f'sign: (E, S) = ({E}, {S})')

#### IV проверка подписи

RR = (pow(G, S, P) * pow(Y, E, P)) % P
print(f'RR={RR}')
EE = abs(hash(f'{M}{RR}'))

assert E == EE, f'E = {E} != {EE} = EE'

if __name__ == '__main__':
    pass
