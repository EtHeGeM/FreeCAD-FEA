#!/usr/bin/env python3
from __future__ import annotations

import math
import re
from pathlib import Path


BASE = Path("shaft_6061_fem_output/Gmsh_Mesh_3mm_8mm_corrected")
if not BASE.with_suffix(".frd").exists():
    BASE = Path("shaft_6061_fem_output/Gmsh_Mesh_3mm_8mm")

FRD = BASE.with_suffix(".frd")
DAT = BASE.with_suffix(".dat")
OUT = Path("shaft_6061_fem_output/extracted_fea_values_corrected.txt")

FLOAT_RE = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[Ee][-+]?\d+)?")


def values_after_node_id(line: str) -> tuple[int, list[float]]:
    node = int(line[3:13])
    vals = [float(x) for x in FLOAT_RE.findall(line[13:])]
    return node, vals


def eigenvalues_symmetric_3x3(sxx, syy, szz, sxy, syz, szx):
    # Jacobi iteration for a 3x3 real symmetric matrix; avoids external deps.
    a = [
        [sxx, sxy, szx],
        [sxy, syy, syz],
        [szx, syz, szz],
    ]
    for _ in range(40):
        p, q = 0, 1
        max_off = abs(a[0][1])
        for i, j in ((0, 2), (1, 2)):
            if abs(a[i][j]) > max_off:
                p, q = i, j
                max_off = abs(a[i][j])
        if max_off < 1.0e-12:
            break
        if abs(a[p][p] - a[q][q]) < 1.0e-30:
            angle = math.pi / 4.0
        else:
            angle = 0.5 * math.atan2(2.0 * a[p][q], a[p][p] - a[q][q])
        c = math.cos(angle)
        s = math.sin(angle)
        app = c * c * a[p][p] + 2 * c * s * a[p][q] + s * s * a[q][q]
        aqq = s * s * a[p][p] - 2 * c * s * a[p][q] + c * c * a[q][q]
        a[p][q] = a[q][p] = 0.0
        a[p][p], a[q][q] = app, aqq
        for k in range(3):
            if k in (p, q):
                continue
            akp = c * a[k][p] + s * a[k][q]
            akq = -s * a[k][p] + c * a[k][q]
            a[k][p] = a[p][k] = akp
            a[k][q] = a[q][k] = akq
    return sorted([a[0][0], a[1][1], a[2][2]], reverse=True)


def von_mises(sxx, syy, szz, sxy, syz, szx):
    return math.sqrt(
        0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2)
        + 3.0 * (sxy**2 + syz**2 + szx**2)
    )


def parse_frd():
    coords = {}
    disp = {}
    stress = {}
    section = "coords"

    for line in FRD.read_text(errors="replace").splitlines():
        if " -4  DISP" in line:
            section = "disp"
            continue
        if " -4  STRESS" in line:
            section = "stress"
            continue
        if line.startswith(" -3"):
            if section != "coords":
                section = "other"
            continue
        if not line.startswith(" -1"):
            continue

        try:
            node, vals = values_after_node_id(line)
        except ValueError:
            continue

        if section == "coords" and len(vals) >= 3:
            coords[node] = vals[:3]
        elif section == "disp" and len(vals) >= 3:
            ux, uy, uz = vals[:3]
            disp[node] = (ux, uy, uz, math.sqrt(ux * ux + uy * uy + uz * uz))
        elif section == "stress" and len(vals) >= 6:
            sxx, syy, szz, sxy, syz, szx = vals[:6]
            p1, p2, p3 = eigenvalues_symmetric_3x3(sxx, syy, szz, sxy, syz, szx)
            vm = von_mises(sxx, syy, szz, sxy, syz, szx)
            tresca = max(abs(p1 - p2), abs(p2 - p3), abs(p1 - p3))
            stress[node] = (sxx, syy, szz, sxy, syz, szx, p1, p2, p3, vm, tresca)
    return coords, disp, stress


def main():
    coords, disp, stress = parse_frd()
    max_disp_node, max_disp = max(disp.items(), key=lambda item: item[1][3])
    max_vm_node, max_stress = max(stress.items(), key=lambda item: item[1][9])
    max_p1_node, max_p1 = max(stress.items(), key=lambda item: item[1][6])
    min_p3_node, min_p3 = min(stress.items(), key=lambda item: item[1][8])

    reaction_text = DAT.read_text(errors="replace").strip() if DAT.exists() else "unavailable"

    lines = [
        "Extracted FEA values from CalculiX FRD/DAT",
        f"FRD file: {FRD}",
        f"Nodes with coordinates: {len(coords)}",
        f"Nodes with displacement results: {len(disp)}",
        f"Nodes with stress results: {len(stress)}",
        "",
        "Maximum displacement:",
        f"  node = {max_disp_node}",
        f"  coordinate = {coords.get(max_disp_node)} mm",
        f"  ux, uy, uz, |u| = {max_disp}",
        "",
        "Maximum Von Mises stress:",
        f"  node = {max_vm_node}",
        f"  coordinate = {coords.get(max_vm_node)} mm",
        f"  Sxx, Syy, Szz, Sxy, Syz, Szx, P1, P2, P3, VM, Tresca = {max_stress}",
        "",
        "Maximum principal stress P1:",
        f"  node = {max_p1_node}",
        f"  coordinate = {coords.get(max_p1_node)} mm",
        f"  P1 = {max_p1[6]}",
        "",
        "Minimum principal stress P3:",
        f"  node = {min_p3_node}",
        f"  coordinate = {coords.get(min_p3_node)} mm",
        f"  P3 = {min_p3[8]}",
        "",
        "Reaction output from DAT:",
        reaction_text,
        "",
    ]
    OUT.write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
