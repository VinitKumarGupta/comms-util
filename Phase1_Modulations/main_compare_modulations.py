import os
import numpy as np
import matplotlib.pyplot as plt
from run_modulation_case import run_modulation_case


def main():
    # Configuration structure for the simulation
    cfg = {
        "seed": 42,
        "num_bits": int(1e5),
        "EbNoVec": np.arange(0, 21, 1),
        "plotEbNo": 12,
        "showClean": True,
        "showNoisy": True,
    }

    np.random.seed(cfg["seed"])

    specs = [
        {"name": "BPSK", "type": "psk", "M": 2, "phaseOffset": 0},
        {"name": "QPSK", "type": "psk", "M": 4, "phaseOffset": np.pi / 4},
        {"name": "8-PSK", "type": "psk", "M": 8, "phaseOffset": np.pi / 8},
        {"name": "8-QAM", "type": "genqam", "M": 8, "phaseOffset": 0},
        {"name": "16-QAM", "type": "qam", "M": 16, "phaseOffset": 0},
        {"name": "64-QAM", "type": "qam", "M": 64, "phaseOffset": 0},
    ]

    results = []
    for spec in specs:
        print(f"Running {spec['name']}...")
        result = run_modulation_case(spec, cfg)
        results.append(result)

        if cfg["showClean"]:
            plt.figure(figsize=(6, 6))
            import plotting.plot_constellation as pc

            pc.plot_constellation(result["txSig"], f"{spec['name']} (No Noise)", result["refConstellation"])
            plt.title(f"{spec['name']} Clean Constellation")
            plt.show()

        if cfg["showNoisy"] and result["rxSigPlot"] is not None:
            plt.figure(figsize=(6, 6))
            import plotting.plot_constellation as pc

            pc.plot_constellation(result["rxSigPlot"], f"{spec['name']} - AWGN at {cfg['plotEbNo']} dB", result["refConstellation"])
            plt.title(f"{spec['name']} Noisy Constellation")
            plt.show()

    import plotting.plot_ber_curve as pbc

    plt.figure(figsize=(8, 6))
    pbc.plot_ber_curve(cfg["EbNoVec"], results)
    plt.title("BER Comparison")
    plt.show()

    os.makedirs("results", exist_ok=True)
    np.savez(
        "results/phase_1_results.npz",
        cfg=cfg,
        specs=specs,
        results=results,
    )
    print("Done. Saved to results/phase_1_results.npz")


if __name__ == "__main__":
    main()
