import itertools
from typing import List, Iterator

KEY = 'Hello world!'.encode()
KEY_SIZE_BYTES = len(KEY)


def swap(s, i, j):
    t = s[i]
    s[i] = s[j]
    s[j] = t


def key_scheduling_algorithm(key: bytes) -> List[int]:
    s = list(range(0, 256))
    j: int = 0
    l = len(key)
    for i in range(0, 256):
        j: int = (j + s[i] + key[i % l]) % 256
        swap(s, i, j)

    return s


def pseudo_random_generation_algorithm(s: List[int]) -> Iterator[int]:
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        swap(s, i, j)
        t = (s[i] + s[j]) % 256
        k = s[t]
        yield k


if __name__ == '__main__':
    c = 0

    s = key_scheduling_algorithm(KEY)
    print(f'first 5 bytes of key sequence: {list(itertools.islice(pseudo_random_generation_algorithm(s), 5))}')

    with open('../mobydick.txt', 'rb') as input:
        with open('in.txt', 'wb') as inp:
            with open('encrypted.txt', 'wb') as out:
                bs = input.read(1)
                s = key_scheduling_algorithm(KEY)
                key_sequence = pseudo_random_generation_algorithm(s)
                while bs != b"" and c < 40:
                    inp.write(bs)

                    k = next(key_sequence)
                    print(f'{c} encrypt with {k}')
                    e = bytes([bs[0] ^ k])

                    out.write(e)

                    c += 1
                    bs = input.read(1)

    c = 0
    with open('encrypted.txt', 'rb') as input:
        with open('decrypted.txt', 'wb') as out:
            bs = input.read(1)
            s = key_scheduling_algorithm(KEY)
            key_sequence = pseudo_random_generation_algorithm(s)
            while bs != b"":
                k = next(key_sequence)
                print(f'{c} decrypt with {k}')
                d = bytes([bs[0] ^ k])

                out.write(d)

                c += 1
                bs = input.read(1)
