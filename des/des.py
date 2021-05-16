import argparse
from typing import Tuple, List

from bitarray import bitarray
from bitarray.util import ba2int, int2ba

IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

S = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

C = [
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
]

D = [
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4,
]

SHIFT_AMOUNT = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
]

K_PERMUTATION = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32,
]

IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25,
]


def get_k_i_c_d(prev_c: bitarray, prev_d: bitarray, i: int) -> Tuple[bitarray, bitarray, bitarray]:
    assert len(prev_c) == 28
    assert len(prev_d) == 28
    assert 0 <= i < 16

    c = circular_left_shift(prev_c, SHIFT_AMOUNT[i])
    assert len(c) == 28

    d = circular_left_shift(prev_d, SHIFT_AMOUNT[i])
    assert len(d) == 28

    cd = c + d
    assert len(cd) == 56

    k_i = bitarray(48)
    for i in range(0, 48):
        k_i[i] = cd[K_PERMUTATION[i] - 1]

    return k_i, c, d


def s_block(b: bitarray, i: int) -> bitarray:
    assert len(b) == 6
    row_bits = bitarray(2)
    row_bits[0] = b[0]
    row_bits[1] = b[5]
    row = ba2int(row_bits)
    assert 0 <= row < 4
    col = ba2int(b[1:4])
    assert 0 <= col < 16
    return int2ba(S[i][row][col], length=4)


def f(r: bitarray, k: bitarray) -> bitarray:
    r_extended = bitarray(48)
    for i in range(0, 48):
        r_extended[i] = r[E[i] - 1]

    r_xor_k = r_extended ^ k
    assert len(r_xor_k) == 48

    after_s_blocks = bitarray(32)
    for i in range(0, 8):
        after_s_blocks[i * 4:i * 4 + 4] = s_block(r_xor_k[i * 6:i * 6 + 6], i)

    permutated = bitarray(32)
    for i in range(0, 32):
        permutated[i] = after_s_blocks[P[i] - 1]

    return permutated


def circular_left_shift(b: bitarray, c: int) -> bitarray:
    return b[c:] + b[:c]


def encrypt_block(bits_permutated, keys) -> bitarray:
    # l = bits_permutated[0:32] # старшие 32 бита
    l = bits_permutated[32:64]
    # r = bits_permutated[32:64] # младшие 32 бита
    r = bits_permutated[0:32]
    for i in range(0, 16):
        k_i = keys[i]
        assert len(k_i) == 48

        next_l = r
        next_r = l ^ f(r, k_i)

        l = next_l
        r = next_r

    rl = r + l
    assert len(rl) == 64

    return rl


def decrypt_block(bits_permutated, keys) -> bitarray:
    # l = bits_permutated[0:32]
    l = bits_permutated[32:64]
    # r = bits_permutated[32:64]
    r = bits_permutated[0:32]
    for i in range(15, -1, -1):
        k_i = keys[i]
        assert len(k_i) == 48

        prev_l = r ^ f(l, k_i)
        prev_r = l

        l = prev_l
        r = prev_r

    rl = r + l
    assert len(rl) == 64

    return rl


def get_keys(k: bitarray) -> List[bitarray]:
    assert len(k) == 64
    k_extended = k
    # for i in range(0, 8):
    #     k_extended[i * 8:i * 8 + 7] = k[i * 7:i * 7 + 7]
    #     k_extended[i * 8 + 7] = 0

    print(f'The 64 bit key is={k_extended.tobytes().decode("utf-8")}')

    c = bitarray(28)
    for i in range(0, 28):
        c[i] = k_extended[C[i] - 1]

    d = bitarray(28)
    for i in range(0, 28):
        d[i] = k_extended[D[i] - 1]

    keys = []
    for i in range(0, 16):
        (k_i, c, d) = get_k_i_c_d(c, d, i)
        assert len(k_i) == 48
        assert len(c) == 28
        assert len(d) == 28
        keys.append(k_i)

    return keys


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--encrypt', action="store_true")
    group.add_argument('-d', '--decrypt', action="store_true")
    parser.add_argument('-b', '--blocks', type=int)
    parser.add_argument('-k', '--key', type=str)
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()

    key_as_bytes = str.encode(args.key)
    assert len(key_as_bytes) == 8, 'key should be 8 bytes'
    k = bitarray()
    k.frombytes(key_as_bytes)
    keys = get_keys(k)

    with open(args.input, 'rb') as input_file:
        with open(args.output, 'wb') as output_file:
            byte_array: bytes = input_file.read(8)
            block_counter = 0
            while byte_array != b"" and (args.blocks is None or block_counter < args.blocks):
                bits = bitarray()
                bits.frombytes(byte_array)

                bits_permutated = bitarray(64)
                for i in range(0, 64):
                    bits_permutated[i] = bits[IP[i] - 1]

                if args.encrypt:
                    rl = encrypt_block(bits_permutated, keys)
                elif args.decrypt:
                    rl = decrypt_block(bits_permutated, keys)

                inversly_permutated = bitarray(64)
                for i in range(0, 64):
                    inversly_permutated[i] = rl[IP_INV[i] - 1]

                output_file.write(inversly_permutated.tobytes())

                block_counter += 1
                byte_array = input_file.read(8)
