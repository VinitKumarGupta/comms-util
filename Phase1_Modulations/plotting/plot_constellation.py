import matplotlib.pyplot as plt
import numpy as np


def plot_constellation(sig, plot_title, ref_const=None):
    sig = np.asarray(sig).flatten()
    plt.scatter(np.real(sig), np.imag(sig), s=8, alpha=0.5)
    if ref_const is not None:
        ref_const = np.asarray(ref_const).flatten()
        plt.scatter(
            np.real(ref_const),
            np.imag(ref_const),
            s=70,
            marker="x",
            linewidths=1.5,
            c="red",
        )
        plt.legend(["Samples", "Reference constellation"], loc="best")
    else:
        plt.legend(["Samples"], loc="best")

    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.axis("equal")
    plt.xlabel("In-Phase")
    plt.ylabel("Quadrature")
    plt.title(plot_title)
