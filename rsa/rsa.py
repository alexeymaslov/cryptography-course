# 15 число полпись Шнорра
import sys
from typing import Tuple


# ax + by = gcd
# gcd, x, y = extended_gcd(a, b)
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_gcd(b % a, a)

    x: int = y1 - (b // a) * x1
    y: int = x1

    return gcd, x, y


p = 31  # 1 байт
q = 11  # 1 байт
ENCRYPTED_WORD_LENGTH_BYTES = 2
N = p * q
phi = (p - 1) * (q - 1)
# E - шифрующая экспонента
# E т.ч. НОД(E, (p - 1) * (q - 1)) = 1
E = 37

print(f'public: N={N}, E={E}')

gcd, d, y = extended_gcd(E, phi)
# print(f'{phi} * {x} + {E} * {d} = {gcd}')
assert gcd == 1, f'gcd={gcd}, E={E}, phi={phi}, d={d}, y={y}'

while d < 0:
    d += phi

assert (d * E) % phi == 1

print(f'private: d={d}, p={p}, q={q}')

m = 2
encrypted = 1
for i in range(0, E):
    encrypted = (encrypted * m) % N

decrypted = 1
for i in range(0, d):
    decrypted = (decrypted * encrypted) % N

assert m == decrypted, f'encrypted={encrypted}, decrypted={decrypted}'

if __name__ == '__main__':
    c = 0
    with open('../mobydick.txt', 'rb') as input:
        with open('in.txt', 'wb') as inp:
            with open('encrypted.txt', 'wb') as out:
                bs = input.read(1)
                while bs != b"" and c < 40:
                    inp.write(bs)
                    m = int.from_bytes(bs, sys.byteorder)

                    encrypted = pow(m, E, N)
                    print(f'{m} encrypted = {encrypted}')

                    ebs = encrypted.to_bytes(ENCRYPTED_WORD_LENGTH_BYTES, sys.byteorder)

                    out.write(ebs)

                    c += 1
                    bs = input.read(1)

    with open('encrypted.txt', 'rb') as input:
        with open('decrypted.txt', 'wb') as out:
            bs = input.read(ENCRYPTED_WORD_LENGTH_BYTES)
            while bs != b"":
                C = int.from_bytes(bs, sys.byteorder)

                decrypted = pow(C, d, N)
                print(f'{C} decrypted = {decrypted}')

                assert decrypted < 256, f'{C} => {decrypted}'

                dbs = decrypted.to_bytes(1, sys.byteorder)
                out.write(dbs)

                bs = input.read(ENCRYPTED_WORD_LENGTH_BYTES)
