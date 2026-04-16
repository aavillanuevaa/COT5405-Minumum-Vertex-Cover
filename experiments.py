"""
experiments.py
--------------
Runs all three experiments comparing Branch-and-Bound vs Greedy 2-Approximation
for the Minimum Vertex Cover problem.

Experiment 1 : Runtime vs Number of Vertices (fixed p = 0.2)
Experiment 2 : Runtime vs Graph Density (fixed n = 20)
Experiment 3 : Approximation Quality — cover size comparison

Results are saved as PNG images in the results/ directory.
"""

import os
import time
import statistics
import matplotlib.pyplot as plt

from graphs import generate_random_graph, verify_vertex_cover
from branchbound import branchbound
from greedy import greedy_vertex_cover

# ----- output directory ----- #
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# ----- configuration ----- #
NUM_TRIALS = 7
TIMEOUT_S  = 30.0
BB_COLOR     = "#e05c5c"
GREEDY_COLOR = "#4a90d9"
RATIO_COLOR  = "#2ca02c"

plt.rcParams.update({
    "font.family"     : "monospace",
    "axes.spines.top" : False,
    "axes.spines.right": False,
    "figure.dpi"      : 150,
})


# ----- helpers ----- #

def measure_runtime_ms(algorithm, graph, n=None):
    # time one call to algorithm, return (elapsed_ms, result)
    start = time.perf_counter()
    result = algorithm(graph, n) if n is not None else algorithm(graph)
    end = time.perf_counter()
    return (end - start) * 1000.0, result


def avg_runtime(algorithm, n, p, trials, is_bb=False):
    # average runtime over several randomly generated graphs
    # returns None if any trial times out (BandB only)
    times = []
    for seed in range(trials):
        graph, edges = generate_random_graph(n, p, seed=seed * 31 + n)
        elapsed, cover = measure_runtime_ms(algorithm, graph, n if is_bb else None)
        assert verify_vertex_cover(cover, edges)
        if is_bb and elapsed / 1000.0 > TIMEOUT_S:
            return None
        times.append(elapsed)
    return statistics.mean(times)


def make_plot(title, xlabel, ylabel, filename):
    # create a blank figure and return (fig, ax) ready to draw on
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig, ax


def save_plot(fig, ax, filename):
    # add legend, save, and close
    ax.legend()
    plt.tight_layout()
    path = os.path.join(RESULTS_DIR, filename)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [Saved] {path}")


# ----- experiment 1 ----- #

def experiment1():
    print("\n" + "="*60)
    print("Experiment 1: Runtime vs Number of Vertices  (p = 0.2)")
    print("="*60)

    p = 0.2

    # collect BandB runtimes (small graphs only)
    bb_sizes, bb_times = [], []
    for n in range(5, 31, 2):
        t = avg_runtime(branchbound, n, p, NUM_TRIALS, is_bb=True)
        if t is None:
            print(f"  BandB n={n} TIMEOUT")
            break
        bb_sizes.append(n)
        bb_times.append(t)
        print(f"  BandB    n={n:3d}  avg={t:10.3f} ms")

    # collect greedy runtimes (much larger graphs)
    greedy_sizes = [10, 50, 100, 250, 500, 1000, 2500, 5000]
    greedy_times = []
    for n in greedy_sizes:
        t = avg_runtime(greedy_vertex_cover, n, p, NUM_TRIALS)
        greedy_times.append(t)
        print(f"  Greedy n={n:5d}  avg={t:10.3f} ms")

    fig, ax = make_plot(
        "Experiment 1 — Runtime vs Number of Vertices (p = 0.20)",
        "Number of vertices (n)", "Average runtime (ms)",
        "exp1_runtime_vs_vertices.png"
    )
    ax.plot(bb_sizes,     bb_times,     "o-", color=BB_COLOR,     linewidth=2, markersize=6, label="Branch-and-Bound")
    ax.plot(greedy_sizes, greedy_times, "s-", color=GREEDY_COLOR, linewidth=2, markersize=6, label="Greedy 2-Approx")
    ax.set_xscale("log")
    ax.set_yscale("log")
    save_plot(fig, ax, "exp1_runtime_vs_vertices.png")

# ----- experiment 2 ----- #

def experiment2():
    print("\n" + "="*60)
    print("Experiment 2: Runtime vs Graph Density  (n = 20)")
    print("="*60)

    n = 20
    probs    = [round(p * 0.1, 1) for p in range(1, 10)]
    bb_times, greedy_times = [], []

    for p in probs:
        t_bb = avg_runtime(branchbound,   n, p, NUM_TRIALS, is_bb=True)
        t_gr = avg_runtime(greedy_vertex_cover, n, p, NUM_TRIALS)
        bb_times.append(t_bb if t_bb else float("nan"))
        greedy_times.append(t_gr)
        print(f"  p={p:.1f}  BandB={t_bb:9.3f} ms   Greedy={t_gr:8.3f} ms")

    fig, ax = make_plot(
        f"Experiment 2 — Runtime vs Graph Density (n = {n})",
        "Edge probability p (graph density)", "Average runtime (ms)",
        "exp2_runtime_vs_density.png"
    )
    ax.plot(probs, bb_times,     "o-", color=BB_COLOR,     linewidth=2, markersize=6, label="Branch-and-Bound")
    ax.plot(probs, greedy_times, "s-", color=GREEDY_COLOR, linewidth=2, markersize=6, label="Greedy 2-Approx")
    ax.set_xticks(probs)
    save_plot(fig, ax, "exp2_runtime_vs_density.png")

# ----- experiment 3 ----- #

def experiment3():
    print("\n" + "="*60)
    print("Experiment 3: Approximation Quality  (p = 0.3)")
    print("="*60)

    p, TRIALS = 0.3, 10
    sizes = list(range(5, 26, 2))
    bb_avgs, greedy_avgs, ratios = [], [], []

    for n in sizes:
        bb_szs, gr_szs, trial_ratios = [], [], []
        for seed in range(TRIALS):
            graph, edges = generate_random_graph(n, p, seed=seed * 17 + n)
            bb_cover     = branchbound(graph, n)
            greedy_cover = greedy_vertex_cover(graph)
            assert verify_vertex_cover(bb_cover,     edges)
            assert verify_vertex_cover(greedy_cover, edges)
            bb_szs.append(len(bb_cover))
            gr_szs.append(len(greedy_cover))
            if len(bb_cover) > 0:
                trial_ratios.append(len(greedy_cover) / len(bb_cover))

        bb_avgs.append(statistics.mean(bb_szs))
        greedy_avgs.append(statistics.mean(gr_szs))
        ratios.append(statistics.mean(trial_ratios) if trial_ratios else 1.0)
        print(f"  n={n:3d}  OPT={bb_avgs[-1]:5.2f}  Greedy={greedy_avgs[-1]:5.2f}  Ratio={ratios[-1]:.4f}")

    # cover size plot
    fig, ax = make_plot(
        "Experiment 3 — Cover Size: Optimal vs Approximation (p = 0.30)",
        "Number of vertices (n)", "Average vertex cover size",
        "exp3_cover_size.png"
    )
    ax.plot(sizes, bb_avgs,     "o-",  color=BB_COLOR,     linewidth=2, markersize=6, label="BandB (optimal)")
    ax.plot(sizes, greedy_avgs, "s--", color=GREEDY_COLOR, linewidth=2, markersize=6, label="Greedy (approx)")
    save_plot(fig, ax, "exp3_cover_size.png")

    # approximation ratio plot
    fig, ax = make_plot(
        "Experiment 3 — Empirical Approximation Ratio (p = 0.30)",
        "Number of vertices (n)", "Approximation ratio (greedy / optimal)",
        "exp3_approx_ratio.png"
    )
    ax.plot(sizes, ratios, "D-", color=RATIO_COLOR, linewidth=2, markersize=6, label="Empirical ratio")
    ax.axhline(y=2.0, color="gray",  linestyle="--", linewidth=1.5, label="Theoretical bound (2x)")
    ax.axhline(y=1.0, color="black", linestyle=":",  linewidth=1,   label="Optimal (1x)")
    ax.set_ylim(0.8, 2.3)
    save_plot(fig, ax, "exp3_approx_ratio.png")


# ----- main ----- #

if __name__ == "__main__":
    experiment1()
    experiment2()
    experiment3()

    print("\n" + "="*60)
    print("All experiments complete. Results saved to:", RESULTS_DIR)
    print("="*60)