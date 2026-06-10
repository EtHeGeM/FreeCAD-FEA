#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Arc


OUT = Path("final_step_drawings")
OUT.mkdir(exist_ok=True)


def arrow(ax, start, end, text="", color="crimson", ms=16):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=ms, lw=2, color=color))
    if text:
        x = (start[0] + end[0]) / 2
        y = (start[1] + end[1]) / 2
        ax.text(x, y, text, color=color, fontsize=10, ha="center", va="center")


def spring(ax, x0, y0, x1, y1, n=8, amp=0.08, color="black"):
    # simple spring between two points
    dx, dy = x1 - x0, y1 - y0
    L = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    pts = [(x0, y0)]
    for i in range(1, n * 2):
        s = i / (n * 2)
        a = amp * (1 if i % 2 else -1)
        pts.append((x0 + s * dx + a * px, y0 + s * dy + a * py))
    pts.append((x1, y1))
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=1.8)


def setup(ax):
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")


def fbd_2256():
    fig, ax = plt.subplots(figsize=(5, 5))
    setup(ax)
    ax.add_patch(Rectangle((-0.55, -0.65), 1.1, 1.3, fc="#b9d7ea", ec="black", lw=1.5))
    ax.plot([-0.9, 0.9], [1.6, 1.6], color="black", lw=3)
    spring(ax, 0, 1.55, 0, 0.65)
    arrow(ax, (0, -0.65), (0, -1.35), r"$F=100\cos(2t)$ N")
    arrow(ax, (0.75, 0.2), (0.75, 0.95), r"$kx$", color="royalblue")
    arrow(ax, (-0.75, 0.2), (-0.75, -0.65), r"$mx''$", color="darkgreen")
    ax.text(0, 0, "m = 40 kg", ha="center", va="center")
    ax.text(0.18, 1.05, "k = 800 N/m", fontsize=10)
    ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.6, 1.9)
    plt.savefig(OUT / "22-56_fbd.png", dpi=180, bbox_inches="tight")
    plt.close()


def fbd_2237():
    fig, ax = plt.subplots(figsize=(5, 5))
    setup(ax)
    ax.plot([0, 0], [0, -4], color="#4aa3c7", lw=8)
    ax.add_patch(Circle((0, 0), 0.12, fc="white", ec="black", lw=1.5))
    ax.text(0.15, 0.1, "O")
    spring(ax, -1.2, -2, -0.08, -2)
    spring(ax, 1.2, -2, 0.08, -2)
    ax.plot([-1.4, -1.4], [-2.4, -1.6], color="black", lw=3)
    ax.plot([1.4, 1.4], [-2.4, -1.6], color="black", lw=3)
    arc = Arc((0, 0), 1.2, 1.2, theta1=260, theta2=300, lw=1.5, color="crimson")
    ax.add_patch(arc)
    arrow(ax, (0.25, -0.55), (0.45, -0.75), r"$\theta$", color="crimson", ms=12)
    arrow(ax, (-0.2, -2), (-0.9, -2), r"$k(2\theta)$", color="royalblue")
    arrow(ax, (0.2, -2), (0.9, -2), r"$k(2\theta)$", color="royalblue")
    ax.text(0.25, -1, "2 m")
    ax.text(0.25, -3, "2 m")
    ax.set_xlim(-2, 2); ax.set_ylim(-4.5, 0.6)
    plt.savefig(OUT / "22-37_fbd.png", dpi=180, bbox_inches="tight")
    plt.close()


def fbd_2223():
    fig, ax = plt.subplots(figsize=(5.5, 4))
    setup(ax)
    ax.add_patch(Circle((0, 0), 1, fc="#b9d7ea", ec="black", lw=1.5))
    ax.add_patch(Circle((0, 0), 0.08, fc="white", ec="black"))
    spring(ax, 0.1, 0.8, 2.4, 0.8)
    spring(ax, 0.1, -0.8, 2.4, -0.8)
    ax.plot([2.6, 2.6], [-1.2, 1.2], color="black", lw=3)
    ax.text(0, -1.25, r"$r=0.150$ m", ha="center")
    arc = Arc((0, 0), 1.6, 1.6, theta1=25, theta2=85, lw=2, color="crimson")
    ax.add_patch(arc)
    arrow(ax, (0.55, 0.55), (0.35, 0.8), r"$\theta$", color="crimson", ms=12)
    ax.text(1.45, 1.05, "k = 80 N/m")
    ax.text(1.45, -1.25, "k = 80 N/m")
    ax.set_xlim(-1.4, 3); ax.set_ylim(-1.6, 1.6)
    plt.savefig(OUT / "22-23_fbd.png", dpi=180, bbox_inches="tight")
    plt.close()


def fbd_726():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    setup(ax)
    ax.plot([0, 1.8], [0, 0], color="#8b5a2b", lw=8)
    arrow(ax, (0.6, 0.8), (0.6, 0.15), r"$P$")
    arrow(ax, (1.2, 0.9), (1.2, 0.15), r"$2P$")
    arrow(ax, (0, -0.8), (0, -0.15), r"$R_A=4P/3$", color="royalblue")
    arrow(ax, (1.8, -0.8), (1.8, -0.15), r"$R_B=5P/3$", color="royalblue")
    for x, label in [(0.3, "0.6 m"), (0.9, "0.6 m"), (1.5, "0.6 m")]:
        ax.text(x, -0.35, label, ha="center", fontsize=9)
    ax.set_xlim(-0.2, 2.0); ax.set_ylim(-1.0, 1.1)
    plt.savefig(OUT / "7-26_fbd.png", dpi=180, bbox_inches="tight")
    plt.close()


def mohr_template():
    fig, ax = plt.subplots(figsize=(5, 4))
    setup(ax)
    c, r = 4, 3
    th = np.linspace(0, 2*np.pi, 400)
    ax.plot(c + r*np.cos(th), r*np.sin(th), lw=2)
    ax.axhline(0, color="black", lw=1)
    ax.axvline(0, color="black", lw=1)
    ax.scatter([1, 7], [0, 0], color="crimson")
    ax.text(1, -0.45, r"$\sigma_2$", ha="center")
    ax.text(7, -0.45, r"$\sigma_1$", ha="center")
    ax.text(c, 0.25, r"$\sigma_{avg}$", ha="center")
    ax.text(c + 1.5, 2.0, r"$R=\tau_{max}$")
    ax.set_xlabel(r"$\sigma$")
    ax.set_ylabel(r"$\tau$")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=.25)
    plt.savefig(OUT / "mohr_template.png", dpi=180, bbox_inches="tight")
    plt.close()


def shaft_section_template():
    fig, ax = plt.subplots(figsize=(5, 4))
    setup(ax)
    ax.add_patch(Circle((0, 0), 1, fc="#e8f1ff", ec="black", lw=1.5))
    arrow(ax, (0, 0), (1.25, 0), r"$c=d/2$", color="black", ms=10)
    arrow(ax, (-1.7, 0.7), (-1.05, 0.7), r"$M$", color="darkorange")
    arrow(ax, (-1.7, -0.7), (-1.05, -0.7), r"$T$", color="crimson")
    ax.text(0, 1.2, r"$\sigma=Mc/I$")
    ax.text(0, -1.35, r"$\tau=Tc/J$")
    ax.text(0.8, 0.25, "surface point")
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-1.7, 1.7)
    plt.savefig(OUT / "shaft_section_template.png", dpi=180, bbox_inches="tight")
    plt.close()


def main():
    fbd_2256()
    fbd_2237()
    fbd_2223()
    fbd_726()
    mohr_template()
    shaft_section_template()


if __name__ == "__main__":
    main()
