# COT5405-Minumum-Vertex-Cover
COT5405 Spring 2026 Course Project. Minimum Vertex Cover Algorithm Analysis

## Overview
This project empirically compares two algorithms for the Minimum Vertex Cover problem:

1. **Branch-and-Bound** — exact solver, O(2^n) worst case
2. **Greedy** — 2-approximation, O(V+E) worst case

## Files
| File | Description |
|------|-------------|
| `graphs.py` | Random graph generation utilities |
| `branchbound.py` | Exact Branch-and-Bound solver |
| `greedy.py` | Greedy 2-Approximation solver |
| `experiments.py` | All three experiments + plot generation |
| `results/` | Folder where output plots are saved (auto-created) |

## Dependencies
- Python 3.7 or later
- matplotlib

```bash
pip install matplotlib
```

## How to Run
```bash
python experiments.py
```

This will automatically:
- Generate random graphs
- Run both algorithms and measure runtimes
- Save result plots as PNG files in the `results/` folder

Expected runtime: 2–10 minutes depending on your machine.

## Experiments
| Experiment | Description | Output |
|------------|-------------|--------|
| Experiment 1 | Runtime vs Number of Vertices (p = 0.2) | `results/exp1_runtime_vs_vertices.png` |
| Experiment 2 | Runtime vs Graph Density (n = 20) | `results/exp2_runtime_vs_density.png` |
| Experiment 3 | Cover Size: Optimal vs Approximation (p = 0.3) | `results/exp3_cover_size.png` |
| Experiment 3 | Empirical Approximation Ratio (p = 0.3) | `results/exp3_approx_ratio.png` |

## Reproducibility
Random seeds are fixed inside `experiments.py`, so every run on the same machine will produce identical results.
