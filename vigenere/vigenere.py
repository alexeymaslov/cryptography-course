import string
from itertools import cycle
from operator import itemgetter

alphabet_size = 26


# a -> 0
# z -> 25
def char_to_number(char: str):
    return ord(char[0]) - ord('a')


# 0 -> a
# 25 -> z
def number_to_char(number: int):
    return chr(number + ord('a'))


def encrypt(key: str, message: str):
    key_as_numbers = [char_to_number(char)
                      for char
                      in key.lower().replace(' ', '')]
    message_as_numbers = [char_to_number(char)
                          for char
                          in message.lower().replace(' ', '')]
    return ''.join(
        [number_to_char((k + c) % alphabet_size)
         for k, c
         in zip(cycle(key_as_numbers), message_as_numbers)]
    )


def ci(m):
    occurencies_of_letters = [m.count(c) for c in string.ascii_lowercase]
    return sum([o * o for o in occurencies_of_letters]) / (len(m) * len(m))


def find_key_length(m):
    text = m
    t = 1
    while True:
        d = ci(text)
        diff = abs(d - 0.065)
        print(f't={t}, d={d}, diff={diff}')
        if diff < 0.001:
            return t

        t += 1
        text = m[1::t]


def find_key(cipher):
    t = find_key_length(cipher)
    grouped_by_mod_t = [cipher[start::t] for start in range(0, t)]
    key = []
    for subtext in grouped_by_mod_t:
        occurencies_of_letter = [(c, subtext.count(c)) for c in string.ascii_lowercase]
        e = max(occurencies_of_letter, key=itemgetter(1))[0]
        c = chr(((ord(e) - ord('e')) % alphabet_size) + ord('a'))
        key.append(c)

    return ''.join(key)


def decrypt(key, cipher):
    key_as_numbers = [char_to_number(char)
                      for char
                      in key.lower().replace(' ', '')]
    cipher_as_numbers = [char_to_number(char)
                         for char
                         in cipher.lower().replace(' ', '')]
    return ''.join(
        [number_to_char((c - k) % alphabet_size)
         for k, c
         in zip(cycle(key_as_numbers), cipher_as_numbers)]
    )


if __name__ == '__main__':
    with open('../mobydick.txt', 'r') as file:
        s = file.read().lower()
        result = ''.join(c for c in s if c.isalpha())
        with open('mobydick_onlyletters_lower.txt', 'w') as out:
            out.write(result)

    with open('mobydick_onlyletters_lower.txt', 'r') as file:
        message = file.read()
    key = 'helloworld'
    print(f'Key: {key}')
    cipher = encrypt(key, message)
    found_key = find_key(cipher)
    print(f'Key found with Kasiski method: {found_key}')
    decrypted_message = decrypt(found_key, cipher)
    with open('mobydick_decrypted.txt', 'w') as out:
        out.write(decrypted_message)

    assert decrypted_message == message
