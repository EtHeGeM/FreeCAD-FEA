#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


OUT_DIR = Path("shaft_6061_fem_output")
SRC = OUT_DIR / "Gmsh_Mesh_3mm_8mm.inp"
FIXED = OUT_DIR / "Gmsh_Mesh_3mm_8mm_corrected.inp"

TARGETS = {
    "End_Axial_100kN_plus_X": 100000.0,
    "End_Vertical_10kN_minus_Y": -10000.0,
    "Middle_20kN_plus_Z": 20000.0,
}


def block_sums(lines: list[str]) -> dict[str, float]:
    current = None
    sums = {}
    for line in lines:
        if line.startswith("** "):
            label = line[3:].strip()
            if label in TARGETS:
                current = label
                sums[current] = 0.0
                continue
            if "node loads" not in label:
                current = None
        if current and line.strip() and not line.startswith("*") and not line.startswith("**"):
            parts = [part.strip() for part in line.split(",")]
            if len(parts) >= 3:
                sums[current] += float(parts[2])
    return sums


def main() -> None:
    lines = SRC.read_text().splitlines()
    sums = block_sums(lines)
    factors = {name: TARGETS[name] / sums[name] for name in TARGETS}

    fixed_lines = []
    current = None
    for line in lines:
        if line.startswith("** "):
            label = line[3:].strip()
            if label in TARGETS:
                current = label
            elif "node loads" not in label:
                current = None
            fixed_lines.append(line)
            continue

        if current and line.strip() and not line.startswith("*") and not line.startswith("**"):
            parts = [part.strip() for part in line.split(",")]
            if len(parts) >= 3:
                parts[2] = f"{float(parts[2]) * factors[current]:.12g}"
                fixed_lines.append(",".join(parts))
                continue
        fixed_lines.append(line)

    FIXED.write_text("\n".join(fixed_lines) + "\n")
    new_sums = block_sums(FIXED.read_text().splitlines())

    print("Original CLOAD totals:")
    for name, total in sums.items():
        print(f"  {name}: {total:g}")
    print("Scale factors:")
    for name, factor in factors.items():
        print(f"  {name}: {factor:g}")
    print("Corrected CLOAD totals:")
    for name, total in new_sums.items():
        print(f"  {name}: {total:g}")

    ccx = shutil.which("ccx")
    if not ccx:
        raise SystemExit("ccx executable not found")

    base = FIXED.with_suffix("")
    print(f"Running: {ccx} {base.name}")
    subprocess.run([ccx, base.name], cwd=OUT_DIR, check=True)


if __name__ == "__main__":
    main()
