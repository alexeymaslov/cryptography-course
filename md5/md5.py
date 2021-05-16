import math
import sys
import hashlib

from bitarray import bitarray
from bitarray._util import ba2hex
from bitarray.util import int2ba


A = 0x01234567
B = 0x89abcdef
C = 0xfedcba98
D = 0x76543210


def F(X, Y, Z):
    return (X & Y) | ((~X) & Z)


def G(X, Y, Z):
    return (X & Z) | ((~Z) & Y)


def H(X, Y, Z):
    return X ^ Y ^ Z


def I(X, Y, Z):
    return Y ^ ((~Z) | X)


T = [int(pow(2, 32) * math.floor(math.sin(n))) for n in range(1, 65)]


def ror(val: int, r_bits: int, max_bits: int = 8) -> int:
    return ((val & (2 ** max_bits - 1)) >> r_bits % max_bits) | \
           (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))


def rol(val: int, r_bits: int, max_bits: int = 8) -> int:
    return (val << r_bits % max_bits) & (2 ** max_bits - 1) | \
           ((val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits)))


# alla_levina@mail.ru

def my_md5(M):
    # print(M)
    bits = bitarray()
    bits.frombytes(M)
    # print(bits)

    original_len_bits = len(bits)

    # добавляем 1
    bits.append(1)
    # print(bits)

    # добавляем нули
    bits_len_mod_512 = len(bits) % 512
    # print(f'len(bits) % 512={len(bits) % 512}')
    if bits_len_mod_512 < 448:
        zeros = bitarray(448 - bits_len_mod_512)
        zeros.setall(0)
        bits.extend(zeros)
    else:
        zeros = bitarray(448 + 512 - bits_len_mod_512)
        zeros.setall(0)
        bits.extend(zeros)
    assert len(bits) % 512 == 448, f'len(bits) % 512={len(bits) % 512}'
    # print(bits)

    # добавляем длину изначального сообщения
    original_len_bits_in_bytes = original_len_bits.to_bytes(8, sys.byteorder)
    bs = bitarray()
    bs.frombytes(original_len_bits_in_bytes[0:4])
    bits.extend(bs)
    bs = bitarray()
    bs.frombytes(original_len_bits_in_bytes[4:8])
    bits.extend(bs)
    # print(bits)
    assert len(bits) % 512 == 0, f'len(bits) % 512={len(bits) % 512}'

    a0 = A
    b0 = B
    c0 = C
    d0 = D

    for i in range(0, len(bits) // 512):
        slice = bits[i * 512:(i + 1) * 512]
        X = [slice[j * 32:(j + 1) * 32] for j in range(0, 16)]
        a = a0
        b = b0
        c = c0
        d = d0

        s_1 = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22]
        for k in range(0, 16):
            x_k = int.from_bytes(X[k].tobytes(), sys.byteorder)
            aa = b + rol(a + F(b, c, d) + x_k + T[k], s_1[k], 32)
            a = d
            d = c
            c = b
            b = aa

        s_2 = [5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20]
        for k in range(0, 16):
            x_k = int.from_bytes(X[k].tobytes(), sys.byteorder)
            aa = b + rol(a + G(b, c, d) + x_k + T[k + 16], s_2[k], 32)
            a = d
            d = c
            c = b
            b = aa

        s_3 = [4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23]
        for k in range(0, 16):
            x_k = int.from_bytes(X[k].tobytes(), sys.byteorder)
            aa = b + rol(a + H(b, c, d) + x_k + T[k + 32], s_3[k], 32)
            a = d
            d = c
            c = b
            b = aa

        s_4 = [6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
        for k in range(0, 16):
            x_k = int.from_bytes(X[k].tobytes(), sys.byteorder)
            aa = b + rol(a + I(b, c, d) + x_k + T[k + 48], s_4[k], 32)
            a = d
            d = c
            c = b
            b = aa

        a0 = (a0 + a) % (2 ** 32)
        b0 = (b0 + b) % (2 ** 32)
        c0 = (c0 + c) % (2 ** 32)
        d0 = (d0 + d) % (2 ** 32)

    total = int2ba(a0, length=32) + int2ba(b0, length=32) + int2ba(c0, length=32) + int2ba(d0, length=32)
    assert len(total) == 128, len(total)

    return total


if __name__ == '__main__':
    # M = 'He visited this country also with a view'.encode()
    M = 'md5'.encode()

    total = my_md5(M)
    total2 = my_md5('md4'.encode())

    print(f'{M}:')
    print(ba2hex(total))
    print('VS')
    hash_object = hashlib.md5(M)
    print(hash_object.hexdigest())

    print(f'"md4":\n{ba2hex(total2)}')