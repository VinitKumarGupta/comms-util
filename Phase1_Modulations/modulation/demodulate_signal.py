import numpy as np
from .symbol_mapping import symbols_to_bits, gray_decode
from .constellations import psk_constellation, qam_constellation, cross_8qam_constellation


def demodulate_signal(rx_sig, spec):
    rx_sig = np.asarray(rx_sig, dtype=np.complex128).flatten()
    if spec["type"] == "psk":
        ref_const = psk_constellation(spec["M"], phase_offset=spec["phaseOffset"])
        angles = np.angle(rx_sig) - spec["phaseOffset"]
        angles = np.mod(angles + np.pi, 2 * np.pi)
        idx = np.round(angles / (2 * np.pi / spec["M"])) .astype(int) % spec["M"]
        rx_sym = gray_decode(idx)
    elif spec["type"] == "qam":
        ref_const = qam_constellation(spec["M"])
        side = int(np.sqrt(spec["M"]))
        norm = np.sqrt(np.mean(np.abs(ref_const) ** 2))
        re = np.real(rx_sig)
        im = np.imag(rx_sig)
        col = np.clip(np.rint(re * norm / 2 + (side - 1) / 2).astype(int), 0, side - 1)
        row = np.clip(np.rint((side - 1) / 2 - im * norm / 2).astype(int), 0, side - 1)
        rx_sym = gray_decode(row) * side + gray_decode(col)
    elif spec["type"] == "genqam":
        ref_const = cross_8qam_constellation()
        distances = np.abs(rx_sig[:, np.newaxis] - ref_const[np.newaxis, :])
        rx_sym = np.argmin(distances, axis=1)
    else:
        raise ValueError(f"Unknown modulation type: {spec['type']}")

    rx_bits = symbols_to_bits(rx_sym, spec["M"])
    rx_bits = rx_bits[: rx_sig.size * int(np.log2(spec["M"]))]
    return rx_bits, rx_sym
