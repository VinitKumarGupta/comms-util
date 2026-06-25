import numpy as np


def bits_to_symbols(bits, k):
    bits = bits.reshape(-1)
    pad_bits = (-bits.size) % k
    if pad_bits > 0:
        bits = np.concatenate([bits, np.zeros(pad_bits, dtype=np.uint8)])
    bit_matrix = bits.reshape(-1, k)
    weights = 2 ** np.arange(k - 1, -1, -1, dtype=int)
    symbols = bit_matrix.dot(weights)
    return symbols.astype(np.int64), bits, pad_bits


def symbols_to_bits(symbols, M):
    k = int(np.log2(M))
    symbols = np.asarray(symbols, dtype=int).flatten()
    bits = np.zeros((symbols.size, k), dtype=np.uint8)
    for idx in range(k):
        bits[:, idx] = (symbols >> (k - idx - 1)) & 1
    return bits.reshape(-1)


def gray_encode(symbols):
    symbols = np.asarray(symbols, dtype=int)
    return symbols ^ (symbols >> 1)


def gray_decode(symbols):
    symbols = np.asarray(symbols, dtype=int)
    decoded = np.zeros_like(symbols)
    for bit in range(symbols.dtype.itemsize * 8):
        decoded ^= symbols >> bit
    return decoded
