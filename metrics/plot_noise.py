"""
metrics/plot_noise.py
Zajérzékenység grafikonok generálása a noise_analysis.py eredményeiből.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metrics.noise_analysis import run_all


def generate_plots(shots: int = 1024):

    # ── Adatok ───────────────────────────────────────────────────────────────

    data        = run_all(shots=shots)
    error_rates = data["error_rates"]
    results     = data["results"]
    error_pct   = [r * 100 for r in error_rates]

    colors  = ['#2563EB', '#16A34A', '#DC2626', '#D97706', '#7C3AED', '#0891B2']
    markers = ['o', 's', '^', 'D', 'v', 'P']

    # ── 1. Zajérzékenység görbék ─────────────────────────────────────────────

    fig, ax = plt.subplots(figsize=(9, 5))

    for i, r in enumerate(results):
        ax.plot(error_pct, r["accuracies"],
                label=r["name"],
                color=colors[i],
                marker=markers[i],
                linewidth=2,
                markersize=5)

    ax.set_xlabel("Depolarizációs hibaarány (%)", fontsize=12)
    ax.set_ylabel("Pontosság", fontsize=12)
    ax.set_title("Kvantum hálózatok zajérzékenysége", fontsize=13, fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.set_ylim(0.10, 1.05)
    ax.set_xlim(-0.2, 21)
    ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='50% pontosság')
    ax.legend(loc='lower left', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig("tests/noise_accuracy.png", dpi=150, bbox_inches='tight')
    print("Mentve: tests/noise_accuracy.png")
    plt.close()

    # ── 2. Pontosság p=0.05-nél (oszlopdiagram) ──────────────────────────────

    idx_5pct = error_rates.index(0.05)
    names    = [r["name"] for r in results]
    accs_5   = [r["accuracies"][idx_5pct] for r in results]

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.bar(names, accs_5, color=colors, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, accs_5):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.01,
                f'{val:.0%}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_ylabel("Pontosság", fontsize=12)
    ax.set_title("Pontosság 5%-os hibaaránynál (p=0.05)", fontsize=13, fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.set_ylim(0, 1.1)
    ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.grid(True, axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=15, ha='right')

    plt.tight_layout()
    plt.savefig("tests/noise_bar_5pct.png", dpi=150, bbox_inches='tight')
    print("Mentve: tests/noise_bar_5pct.png")
    plt.close()

    # ── 3. Összehasonlító metrikák oszlopdiagram ──────────────────────────────

    metrics = {
        "Féladder":         {"gate_count": 2,  "q_gate_count": 4,  "depth": 1, "q_depth": 3,  "ancilla": 1},
        "Teljes összeadó":  {"gate_count": 5,  "q_gate_count": 8,  "depth": 3, "q_depth": 6,  "ancilla": 1},
        "Paritásgenerátor": {"gate_count": 3,  "q_gate_count": 6,  "depth": 3, "q_depth": 4,  "ancilla": 1},
        "Majority gate":    {"gate_count": 5,  "q_gate_count": 6,  "depth": 3, "q_depth": 4,  "ancilla": 1},
        "Multiplexer":      {"gate_count": 9,  "q_gate_count": 16, "depth": 3, "q_depth": 10, "ancilla": 1},
        "Komparátor":       {"gate_count": 17, "q_gate_count": 56, "depth": 6, "q_depth": 30, "ancilla": 4},
    }

    labels   = list(metrics.keys())
    cl_gates = [metrics[n]["gate_count"]   for n in labels]
    qu_gates = [metrics[n]["q_gate_count"] for n in labels]
    cl_depth = [metrics[n]["depth"]        for n in labels]
    qu_depth = [metrics[n]["q_depth"]      for n in labels]

    x     = np.arange(len(labels))
    width = 0.35

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    ax1 = axes[0]
    b1  = ax1.bar(x - width/2, cl_gates, width, label='Klasszikus', color='#2563EB', alpha=0.85)
    b2  = ax1.bar(x + width/2, qu_gates, width, label='Kvantum',    color='#DC2626', alpha=0.85)
    ax1.set_title("Kapuszám összehasonlítás", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Kapuszám", fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=20, ha='right', fontsize=9)
    ax1.legend(fontsize=10)
    ax1.grid(True, axis='y', alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    for bar in b1:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 str(int(bar.get_height())), ha='center', va='bottom', fontsize=9)
    for bar in b2:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 str(int(bar.get_height())), ha='center', va='bottom', fontsize=9)

    ax2 = axes[1]
    b3  = ax2.bar(x - width/2, cl_depth, width, label='Klasszikus', color='#2563EB', alpha=0.85)
    b4  = ax2.bar(x + width/2, qu_depth, width, label='Kvantum',    color='#DC2626', alpha=0.85)
    ax2.set_title("Áramköri mélység összehasonlítás", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Mélység", fontsize=11)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=20, ha='right', fontsize=9)
    ax2.legend(fontsize=10)
    ax2.grid(True, axis='y', alpha=0.3)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    for bar in b3:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 str(int(bar.get_height())), ha='center', va='bottom', fontsize=9)
    for bar in b4:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 str(int(bar.get_height())), ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig("tests/metrics_comparison.png", dpi=150, bbox_inches='tight')
    print("Mentve: tests/metrics_comparison.png")
    plt.close()

    print("\nMinden grafikon elkészült!")


if __name__ == "__main__":
    generate_plots(shots=1024)