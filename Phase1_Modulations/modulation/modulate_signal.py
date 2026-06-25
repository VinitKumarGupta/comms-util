import numpy as np
from .symbol_mapping import bits_to_symbols, gray_encode
from .constellations import psk_constellation, qam_constellation, cross_8qam_constellation


def modulate_signal(bits_in, spec):
    bits_in = np.asarray(bits_in, dtype=np.uint8).flatten()
    k = int(np.log2(spec["M"]))
    tx_sym, tx_bits_padded, pad_bits = bits_to_symbols(bits_in, k)

    if spec["type"] == "psk":
        ref_const = psk_constellation(spec["M"], phase_offset=spec["phaseOffset"])
        tx_sig = ref_const[gray_encode(tx_sym)]
    elif spec["type"] == "qam":
        ref_const = qam_constellation(spec["M"])
        tx_sig = ref_const[tx_sym]
    elif spec["type"] == "genqam":
        ref_const = cross_8qam_constellation()
        tx_sig = ref_const[tx_sym]
    else:
        raise ValueError(f"Unknown modulation type: {spec['type']}")

    return tx_sig, tx_bits_padded, pad_bits, tx_sym, ref_const
