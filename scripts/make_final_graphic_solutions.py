#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path("final_graphic_solutions")
OUT.mkdir(exist_ok=True)


def savefig(name: str):
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=180)
    plt.close()


def vibration_2256():
    m, k, F0, w = 40.0, 800.0, 100.0, 2.0
    wn = math.sqrt(k / m)
    X = F0 / abs(k - m * w * w)
    vmax = w * X
    t = np.linspace(0, 2 * math.pi / w, 500)
    x = X * np.cos(w * t)
    v = -w * X * np.sin(w * t)
    fig, ax = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
    ax[0].plot(t, x, lw=2)
    ax[0].set_ylabel("x_ss [m]")
    ax[0].set_title(f"22-56 steady-state response: wn={wn:.3f} rad/s, vmax={vmax:.4f} m/s")
    ax[0].grid(True, alpha=.3)
    ax[1].plot(t, v, color="crimson", lw=2)
    ax[1].axhline(vmax, color="k", ls="--", lw=1)
    ax[1].axhline(-vmax, color="k", ls="--", lw=1)
    ax[1].set_ylabel("v [m/s]")
    ax[1].set_xlabel("t [s]")
    ax[1].grid(True, alpha=.3)
    savefig("22-56_response.png")


def rod_spring_2237():
    theta = np.linspace(-0.18, 0.18, 200)
    k = 200
    m = 6
    L = 4
    I = m * L**2 / 3
    Ktheta = 8 * k
    wn = math.sqrt(Ktheta / I)
    M = -Ktheta * theta
    plt.figure(figsize=(7, 4))
    plt.plot(theta, M, lw=2)
    plt.axhline(0, color="k", lw=.8)
    plt.axvline(0, color="k", lw=.8)
    plt.grid(True, alpha=.3)
    plt.xlabel(r"small rotation $\theta$ [rad]")
    plt.ylabel(r"restoring moment $M_s$ [N m]")
    plt.title(f"22-37 restoring moment: Ktheta=8k={Ktheta:.0f} N m/rad, wn={wn:.3f} rad/s")
    savefig("22-37_restoring_moment.png")


def beam_726():
    # Beam length 1.8 m, loads P at 0.6 m and 2P at 1.2 m.
    P = 1.0
    L = 1.8
    xs = np.linspace(0, L, 500)
    RA = (P*(L-0.6)+2*P*(L-1.2))/L
    RB = 3*P - RA
    V = np.where(xs < 0.6, RA, np.where(xs < 1.2, RA-P, RA-3*P))
    M = RA*xs - P*np.maximum(xs-0.6, 0) - 2*P*np.maximum(xs-1.2, 0)
    fig, ax = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
    ax[0].plot(xs, V, lw=2)
    ax[0].fill_between(xs, 0, V, alpha=.15)
    ax[0].set_ylabel("V / P")
    ax[0].grid(True, alpha=.3)
    ax[0].set_title(f"7-26 shear and moment diagrams: RA={RA:.3f}P, RB={RB:.3f}P")
    ax[1].plot(xs, M, color="darkorange", lw=2)
    ax[1].fill_between(xs, 0, M, alpha=.15, color="darkorange")
    ax[1].set_ylabel("M / P [m]")
    ax[1].set_xlabel("x [m]")
    ax[1].grid(True, alpha=.3)
    savefig("7-26_shear_moment.png")


def mohr_circle(name: str, sx: float, sy: float, txy: float, title: str):
    c = 0.5 * (sx + sy)
    r = math.sqrt(((sx - sy) / 2) ** 2 + txy**2)
    th = np.linspace(0, 2 * math.pi, 500)
    plt.figure(figsize=(5.7, 5.2))
    plt.plot(c + r * np.cos(th), r * np.sin(th), lw=2)
    plt.scatter([sx, sy], [txy, -txy], c=["crimson", "navy"], zorder=5)
    plt.axhline(0, color="k", lw=.8)
    plt.axvline(0, color="k", lw=.8)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.grid(True, alpha=.3)
    plt.xlabel(r"normal stress $\sigma$ [MPa]")
    plt.ylabel(r"shear stress $\tau$ [MPa]")
    plt.title(f"{title}\nσ1={c+r:.2f} MPa, σ2={c-r:.2f} MPa, τmax={r:.2f} MPa")
    savefig(name)


def stress_examples():
    # 9-63 helicopter: d=150 mm, P=225 kN, T=15 kN m
    d = 150.0
    P = 225e3
    T = 15e6
    A = math.pi * d**2 / 4
    J = math.pi * d**4 / 32
    sx = P / A
    tau = T * (d/2) / J
    mohr_circle("9-63_mohr.png", sx, 0, tau, "9-63 helicopter shaft")

    # 10-69 concrete cylinder: d=50 mm, T=500 N m, P=-2 kN compression
    d = 50.0
    P = -2000.0
    T = 500e3
    A = math.pi * d**2 / 4
    J = math.pi * d**4 / 32
    sx = P / A
    tau = T * (d/2) / J
    mohr_circle("10-69_mohr.png", sx, 0, tau, "10-69 concrete cylinder")


def pressure_vessel():
    p, r, t, E, nu = 15e6, 0.5, 0.01, 200e9, 0.3
    hoop = p*r/t
    long = p*r/(2*t)
    eh = (hoop - nu*long)/E
    el = (long - nu*hoop)/E
    dd = eh
    dL = el
    labels = ["hoop strain", "longitudinal strain", "diameter inc. [mm]", "length inc. [mm]"]
    vals = [eh*1e6, el*1e6, (2*r*eh)*1000, (3*el)*1000]
    plt.figure(figsize=(8, 4))
    bars = plt.bar(labels, vals, color=["#4477aa", "#66c2a5", "#dd8452", "#c44e52"])
    plt.ylabel("microstrain or mm")
    plt.title("10-56 pressure vessel strain and dimension increases")
    plt.grid(axis="y", alpha=.3)
    for b, v in zip(bars, vals):
        plt.text(b.get_x()+b.get_width()/2, v, f"{v:.3g}", ha="center", va="bottom", fontsize=9)
    savefig("10-56_pressure_vessel.png")


def shear_circle_distribution():
    y = np.linspace(-1, 1, 400)
    tau = 1.5 * (1 - y**2)
    plt.figure(figsize=(6, 4))
    plt.plot(tau, y, lw=2)
    plt.axvline(1, color="k", ls="--", label="average")
    plt.xlabel(r"$\tau/\tau_{avg}$")
    plt.ylabel(r"$y/c$")
    plt.title("7-18 circular rod transverse shear distribution")
    plt.legend()
    plt.grid(True, alpha=.3)
    savefig("7-18_shear_distribution.png")


def main():
    vibration_2256()
    rod_spring_2237()
    beam_726()
    stress_examples()
    pressure_vessel()
    shear_circle_distribution()


if __name__ == "__main__":
    main()
