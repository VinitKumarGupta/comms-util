import matplotlib.pyplot as plt


def plot_ber_curve(EbNoVec, results):
    colors = [
        [0, 0.4470, 0.7410],
        [0.8500, 0.3250, 0.0980],
        [0.4660, 0.6740, 0.1880],
        [0.4940, 0.1840, 0.5560],
        [0.3010, 0.7450, 0.9330],
        [0, 0, 0],
    ]

    for i, result in enumerate(results):
        plt.semilogy(
            EbNoVec,
            result["berSim"],
            "-o",
            color=colors[i % len(colors)],
            linewidth=1.6,
            label=f"{result['name']} Sim",
        )
        if result["berTheory"] is not None and not all(map(lambda x: x != x, result["berTheory"])):
            plt.semilogy(
                EbNoVec,
                result["berTheory"],
                "--",
                color=colors[i % len(colors)],
                linewidth=1.6,
                label=f"{result['name']} Theory",
            )

    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.ylim([1e-6, 1])
    plt.xlabel("Eb/N0 (dB)")
    plt.ylabel("BER")
    plt.title("BER vs Eb/N0")
    plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5))
    plt.tight_layout()
