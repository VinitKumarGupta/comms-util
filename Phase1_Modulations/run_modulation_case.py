import math
import numpy as np
from modulation.modulate_signal import modulate_signal
from modulation.demodulate_signal import demodulate_signal
from channel.add_awgn_noise import add_awgn_noise
from metrics.compute_ber import compute_ber


def erfc_array(x):
    x = np.asarray(x, dtype=float)
    return np.vectorize(math.erfc)(x)


def compute_theoretical_ber(ebno_db, spec_type, M):
    ebno = 10 ** (ebno_db / 10)
    if spec_type == "psk":
        # Approximate BER for M-ary PSK in AWGN using exact formula for coherent BPSK/QPSK and an approximation for M>4.
        if M == 2:
            return 0.5 * np.exp(-ebno)
        elif M == 4:
            return 0.5 * np.exp(-ebno)
        else:
            k = np.log2(M)
            return 2 / k * erfc_array(np.sqrt(ebno) * np.sin(np.pi / M))
    elif spec_type == "qam":
        k = np.log2(M)
        q = np.sqrt(M)
        return 4 * (1 - 1 / q) / k * 0.5 * erfc_array(np.sqrt(3 * k * ebno / (2 * (M - 1))))
    return np.full(np.shape(ebno_db), np.nan, dtype=float)


def run_modulation_case(spec, cfg):
    bits_in = np.random.randint(0, 2, size=(cfg["num_bits"],), dtype=np.uint8)
    k = int(np.log2(spec["M"]))

    tx_sig, tx_bits_padded, pad_bits, tx_sym, ref_const = modulate_signal(bits_in, spec)

    rx_bits_clean, rx_sym_clean = demodulate_signal(tx_sig, spec)
    num_orig_bits = bits_in.size
    ber_clean, err_clean = compute_ber(bits_in, rx_bits_clean[:num_orig_bits])

    ber_sim = np.zeros_like(cfg["EbNoVec"], dtype=float)
    err_count = np.zeros_like(cfg["EbNoVec"], dtype=int)
    rx_sig_plot = None
    rx_bits_plot = None
    rx_sym_plot = None

    for ii, EbNo in enumerate(cfg["EbNoVec"]):
        rx_sig, noise_var, snr_db = add_awgn_noise(tx_sig, EbNo, k)
        rx_bits, rx_sym = demodulate_signal(rx_sig, spec)
        ber_sim[ii], err_count[ii] = compute_ber(bits_in, rx_bits[:num_orig_bits])

        if np.isclose(EbNo, cfg["plotEbNo"]):
            rx_sig_plot = rx_sig
            rx_bits_plot = rx_bits
            rx_sym_plot = rx_sym

    ber_theory = compute_theoretical_ber(cfg["EbNoVec"], spec["type"], spec["M"]) if spec["type"] in {"psk", "qam"} else np.full(cfg["EbNoVec"].shape, np.nan)

    return {
        "name": spec["name"],
        "type": spec["type"],
        "M": spec["M"],
        "bitsPerSymbol": k,
        "bitsIn": bits_in,
        "txSig": tx_sig,
        "txSym": tx_sym,
        "txBitsPadded": tx_bits_padded,
        "padBits": pad_bits,
        "refConstellation": ref_const,
        "rxSigPlot": rx_sig_plot,
        "rxBitsPlot": rx_bits_plot,
        "rxSymPlot": rx_sym_plot,
        "berClean": ber_clean,
        "errClean": err_clean,
        "berSim": ber_sim,
        "errCount": err_count,
        "berTheory": ber_theory,
    }
