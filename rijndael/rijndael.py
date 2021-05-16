from typing import List

from pyfinite import ffield

EXAMPLE_STATE = [b'He v', b'isit', b'ed t', b'his ']

BLOCK_SIZE_BYTES = 24
KEY_SIZE_BYTES = 16
BLOCKS = 4
KEY: bytes = 'hello world!!!!!'.encode()
N_K: int = KEY_SIZE_BYTES // 4
assert N_K <= 6, 'N_K > 6 is not implemented'
N_B: int = BLOCK_SIZE_BYTES // 4

N_R_BY_N_K_AND_N_B = {
    4: {
        4: 10,
        6: 12,
        8: 14,
    },
    6: {
        4: 12,
        6: 12,
        8: 14,
    },
    8: {
        4: 14,
        6: 14,
        8: 14,
    }
}

N_R = N_R_BY_N_K_AND_N_B[N_K][N_B]

C1 = 1
C2 = 2 if N_B == 4 or N_B == 6 else 3
C3 = 3 if N_B == 4 or N_B == 6 else 4

F = ffield.FField(8, gen=0x11b, useLUT=0)
assert F.Multiply(0x57, 0x83) == 0xc1


def ror(val: int, r_bits: int, max_bits: int = 8) -> int:
    return ((val & (2 ** max_bits - 1)) >> r_bits % max_bits) | \
           (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))


def rol(val: int, r_bits: int, max_bits: int = 8) -> int:
    return (val << r_bits % max_bits) & (2 ** max_bits - 1) | \
           ((val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits)))


def s_box(b: int):
    b_inv = F.Inverse(b)
    s = b_inv ^ rol(b_inv, 1) ^ rol(b_inv, 2) ^ rol(b_inv, 3) ^ rol(b_inv, 4) ^ 0x63
    return s


def inv_s_box(s: int):
    b_inv = rol(s, 1) ^ rol(s, 3) ^ rol(s, 6) ^ 0x5
    b = F.Inverse(b_inv)
    return b


assert inv_s_box(s_box(11)) == 11
assert s_box(inv_s_box(11)) == 11

assert s_box(0x00) == 0x63
assert s_box(0x10) == 0xca
assert s_box(0x01) == 0x7c
assert s_box(0x11) == 0x82

# rc: List[int] = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
rc: List[int] = []
for i in range(0, 24):
    if i == 0:
        rc.append(1)
    else:
        rc_prev = rc[i - 1]
        if rc_prev < 0x80:
            rc.append(2 * rc_prev)
        else:
            rc.append((2 * rc_prev) ^ 0x11b)

rcon: List[bytes] = list(map(lambda x: bytes([x, 0, 0, 0]), rc))


def byte_sub(state):
    return list(
        map(
            lambda col: bytes(map(s_box, col)),
            state
        )
    )


def inv_byte_sub(state):
    return list(
        map(
            lambda col: bytes(map(inv_s_box, col)),
            state
        )
    )


assert inv_byte_sub(byte_sub(EXAMPLE_STATE)) == EXAMPLE_STATE
assert byte_sub(inv_byte_sub(EXAMPLE_STATE)) == EXAMPLE_STATE


def shift_row(state, c1, c2, c3, n_b):
    return [
        bytes([
            state[i][0],
            state[(i + c1) % n_b][1],
            state[(i + c2) % n_b][2],
            state[(i + c3) % n_b][3],
        ])
        for i, x in enumerate(state)
    ]


def inv_shift_row(state, c1, c2, c3, n_b):
    return [
        bytes([
            state[i][0],
            state[(i - c1) % n_b][1],
            state[(i - c2) % n_b][2],
            state[(i - c3) % n_b][3],
        ])
        for i, x in enumerate(state)
    ]


assert inv_shift_row(shift_row(EXAMPLE_STATE, 1, 2, 3, 4), 1, 2, 3, 4) == EXAMPLE_STATE
assert shift_row(inv_shift_row(EXAMPLE_STATE, 1, 2, 3, 4), 1, 2, 3, 4) == EXAMPLE_STATE


def mix_column(col: bytes) -> bytes:
    m: List[int] = [
        F.Multiply(2, col[0]) ^ F.Multiply(3, col[1]) ^ col[2] ^ col[3],
        col[0] ^ F.Multiply(2, col[1]) ^ F.Multiply(3, col[2]) ^ col[3],
        col[0] ^ col[1] ^ F.Multiply(2, col[2]) ^ F.Multiply(3, col[3]),
        F.Multiply(3, col[0]) ^ col[1] ^ col[2] ^ F.Multiply(2, col[3]),
    ]

    return bytes(map(lambda x: 255 if x >= 256 else x, m))


assert mix_column(bytes([0xdb, 0x13, 0x53, 0x45])) == \
       bytes([0x8e, 0x4d, 0xa1, 0xbc]), \
    f'Got unexpected result={list(map(lambda x: hex(x), mix_column(bytes([0xdb, 0x13, 0x53, 0x45]))))} after mixColumn'


def inv_mix_column(col: bytes) -> bytes:
    m: List[int] = [
        F.Multiply(14, col[0]) ^ F.Multiply(11, col[1]) ^ F.Multiply(13, col[2]) ^ F.Multiply(9, col[3]),
        F.Multiply(9, col[0]) ^ F.Multiply(14, col[1]) ^ F.Multiply(11, col[2]) ^ F.Multiply(13, col[3]),
        F.Multiply(13, col[0]) ^ F.Multiply(9, col[1]) ^ F.Multiply(14, col[2]) ^ F.Multiply(11, col[3]),
        F.Multiply(11, col[0]) ^ F.Multiply(13, col[1]) ^ F.Multiply(9, col[2]) ^ F.Multiply(14, col[3]),
    ]

    return bytes(map(lambda x: 255 if x >= 256 else x, m))


assert inv_mix_column(mix_column(bytes([0xdb, 0x13, 0x53, 0x45]))) == bytes([0xdb, 0x13, 0x53, 0x45])
assert mix_column(inv_mix_column(bytes([0xdb, 0x13, 0x53, 0x45]))) == bytes([0xdb, 0x13, 0x53, 0x45])


def mix_columns(state: List[bytes]) -> List[bytes]:
    return list(
        map(
            mix_column,
            state
        )
    )


def inv_mix_columns(state: List[bytes]) -> List[bytes]:
    return list(
        map(
            inv_mix_column,
            state
        )
    )


assert inv_mix_columns(mix_columns(EXAMPLE_STATE)) == EXAMPLE_STATE
assert mix_columns(inv_mix_columns(EXAMPLE_STATE)) == EXAMPLE_STATE


def sub_byte(bs: bytes) -> bytes:
    return bytes(map(s_box, bs))


def rot_byte(bs: bytes) -> bytes:
    return bytes([bs[1], bs[2], bs[3], bs[0]])


def key_expansion(key: bytes) -> List[bytes]:
    w: List[bytes] = []
    for i in range(0, N_K):
        w.append(key[4 * i: 4 * i + 4])

    for i in range(N_K, N_B * (N_R + 1)):
        t: bytes = w[i - 1]
        if i % N_K == 0:
            t: bytes = bytes(map(lambda x, y: x ^ y, sub_byte(rot_byte(t)), rcon[i // N_K - 1]))
        w.append(bytes(map(lambda x, y: x ^ y, w[i - N_K], t)))

    return w


def add_round_key(state: List[bytes], round_key: List[bytes]):
    return list(
        map(
            lambda xs, ys: bytes(map(lambda x, y: x ^ y, xs, ys)),
            state,
            round_key
        )
    )


def rijndael_encrypt(state: List[bytes], key: bytes) -> List[bytes]:
    expanded_key = key_expansion(key)

    state = add_round_key(state, expanded_key[0:N_B])

    for i in range(1, N_R):
        state = byte_sub(state)
        state = shift_row(state, C1, C2, C3, N_B)
        state = mix_columns(state)
        state = add_round_key(state, expanded_key[i * N_B:i * N_B + N_B])

    # final round
    state = byte_sub(state)
    state = shift_row(state, C1, C2, C3, N_B)
    state = add_round_key(state, expanded_key[N_B * N_R: N_B * N_R + N_B])
    return state


def rijndael_decrypt(state: List[bytes], key: bytes) -> List[bytes]:
    expanded_key = key_expansion(key)

    state = add_round_key(state, expanded_key[N_B * N_R: N_B * N_R + N_B])
    state = inv_shift_row(state, C1, C2, C3, N_B)
    state = inv_byte_sub(state)

    for i in range(N_R - 1, 0, -1):
        state = add_round_key(state, expanded_key[i * N_B:i * N_B + N_B])
        state = inv_mix_columns(state)
        state = inv_shift_row(state, C1, C2, C3, N_B)
        state = inv_byte_sub(state)

    state = add_round_key(state, expanded_key[0: N_B])
    return state


if __name__ == '__main__':
    c = 0
    with open('../mobydick.txt', 'rb') as input:
        with open('in.txt', 'wb') as inp:
            with open('encrypted.txt', 'wb') as out:
                bs = input.read(BLOCK_SIZE_BYTES)
                while bs != b"" and c < BLOCKS:
                    inp.write(bs)

                    state = list(
                        map(
                            lambda i: bs[i * 4: i * 4 + 4],
                            range(0, N_B)
                        )
                    )

                    e = rijndael_encrypt(state, KEY)

                    flattened = bytes([x for xs in e for x in xs])

                    out.write(flattened)

                    c += 1
                    bs = input.read(BLOCK_SIZE_BYTES)

    with open('encrypted.txt', 'rb') as input:
        with open('decrypted.txt', 'wb') as out:
            bs = input.read(BLOCK_SIZE_BYTES)
            while bs != b"":
                state = list(
                    map(
                        lambda i: bs[i * 4: i * 4 + 4],
                        range(0, N_B)
                    )
                )

                e = rijndael_decrypt(state, KEY)

                flattened = bytes([x for xs in e for x in xs])

                out.write(flattened)

                bs = input.read(BLOCK_SIZE_BYTES)
