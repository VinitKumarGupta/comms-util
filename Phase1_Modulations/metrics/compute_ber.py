import numpy as np


def compute_ber(tx_bits, rx_bits):
    tx_bits = np.asarray(tx_bits, dtype=np.uint8).flatten()
    rx_bits = np.asarray(rx_bits, dtype=np.uint8).flatten()
    n = min(tx_bits.size, rx_bits.size)
    tx_bits = tx_bits[:n]
    rx_bits = rx_bits[:n]
    num_err = int(np.sum(tx_bits != rx_bits))
    ber = num_err / n if n > 0 else 0.0
    return ber, num_err
