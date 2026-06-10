#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from extract_fea_values import eigenvalues_symmetric_3x3, parse_frd, von_mises


OUT_DIR = Path("freecad_screenshots")
OUT_DIR.mkdir(exist_ok=True)


def result_arrays():
    coords, disp, stress = parse_frd()
    rows = []
    for node, c in coords.items():
        if node not in disp or node not in stress:
            continue
        s = stress[node]
        rows.append(
            {
                "node": node,
                "x": c[0],
                "y": c[1],
                "z": c[2],
                "u": disp[node][3],
                "vm": s[9],
                "p1": s[6],
                "p3": s[8],
            }
        )
    return rows


def scatter_plot(rows, key: str, title: str, filename: str, cmap: str = "turbo"):
    fig = plt.figure(figsize=(14, 6), dpi=160)
    ax = fig.add_subplot(111)
    xs = [r["x"] for r in rows]
    zs = [r["z"] for r in rows]
    vals = [r[key] for r in rows]
    sc = ax.scatter(xs, zs, c=vals, s=13, cmap=cmap, edgecolors="none")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("z [mm]")
    ax.set_title(title)
    ax.grid(True, linewidth=0.3, alpha=0.35)
    cb = fig.colorbar(sc, ax=ax, pad=0.015)
    cb.set_label(title.split("[")[-1].rstrip("]") if "[" in title else key)
    fig.tight_layout()
    fig.savefig(OUT_DIR / filename)
    plt.close(fig)


def main():
    rows = result_arrays()
    scatter_plot(rows, "vm", "Corrected FEA Von Mises Stress [MPa]", "04_corrected_von_mises.png")
    scatter_plot(rows, "p1", "Corrected FEA Principal Stress sigma_1 [MPa]", "05_corrected_principal_sigma1.png")
    scatter_plot(rows, "p3", "Corrected FEA Principal Stress sigma_3 [MPa]", "06_corrected_principal_sigma3.png", cmap="coolwarm")
    scatter_plot(rows, "u", "Corrected FEA Displacement Magnitude [mm]", "07_corrected_displacement.png")
    print(f"Saved corrected result plots to {OUT_DIR}")


if __name__ == "__main__":
    main()
