import numpy as np


def add_awgn_noise(tx_sig, EbNo_db, bits_per_symbol):
    tx_sig = np.asarray(tx_sig, dtype=np.complex128).flatten()
    tx_power = np.mean(np.abs(tx_sig) ** 2)
    snr_db = EbNo_db + 10 * np.log10(bits_per_symbol)
    snr_lin = 10 ** (snr_db / 10)
    noise_var = tx_power / snr_lin
    noise = np.sqrt(noise_var / 2) * (
        np.random.randn(tx_sig.size) + 1j * np.random.randn(tx_sig.size)
    )
    rx_sig = tx_sig + noise
    return rx_sig, noise_var, snr_db
