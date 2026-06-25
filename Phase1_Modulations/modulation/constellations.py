import numpy as np


def psk_constellation(M, phase_offset=0.0):
    theta = 2 * np.pi * np.arange(M) / M + phase_offset
    constellation = np.exp(1j * theta)
    constellation /= np.sqrt(np.mean(np.abs(constellation) ** 2))
    return constellation


def qam_constellation(M):
    side = int(np.sqrt(M))
    if side * side != M:
        raise ValueError("QAM constellation size must be a perfect square")

    row = np.arange(M) // side
    col = np.arange(M) % side
    x = 2 * (col - (side - 1) / 2)
    y = 2 * ((side - 1) / 2 - row)
    constellation = x + 1j * y
    norm = np.sqrt(np.mean(np.abs(constellation) ** 2))
    constellation = constellation / norm

    gray_row = gray_code(row)
    gray_col = gray_code(col)
    gray_index = gray_row * side + gray_col

    ref_const = constellation[gray_index]
    return ref_const


def gray_code(values):
    values = np.asarray(values, dtype=int)
    return values ^ (values >> 1)


def cross_8qam_constellation():
    const = np.array([
        -1 - 1j,
        -1 + 1j,
         1 + 1j,
         1 - 1j,
        -3 + 0j,
         0 + 3j,
         3 + 0j,
         0 - 3j,
    ], dtype=complex)
    const /= np.sqrt(np.mean(np.abs(const) ** 2))
    return const
