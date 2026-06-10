# MECT2222 Term Project Report

## Combined Loading Analysis and FEA Validation

**Student name:** ........................................  
**Student ID:** ........................................  
**Assigned problem:** Cantilever circular shaft under combined axial and transverse loading  
**Date:** 10 June 2026

---

## 1. Introduction and Assumptions

This report analyzes a solid circular shaft subjected to combined axial and transverse loading. The objective is to determine the critical internal loads, stress state, principal stresses, failure-theory equivalent stresses, and factor of safety by analytical mechanics, then compare the results with a finite element model prepared in FreeCAD/CalculiX.

The analyzed member is a solid cylindrical cantilever shaft fixed at the left end. The shaft axis is the global x-axis.

### Geometry

| Parameter | Symbol | Value |
|---|---:|---:|
| Shaft length | L | 600 mm |
| Radius | r | 30 mm |
| Diameter | d | 60 mm |
| Middle transverse load location | a | 400 mm from fixed end |

**Assumed dimension:** The shaft is assumed to be a solid circular cylinder with **diameter d = 60 mm**.

Section properties:

\[
A=\pi r^2=\pi(30)^2=2827.43\ \text{mm}^2
\]

\[
I_y=I_z={\pi r^4\over4}={\pi(30)^4\over4}=636172.51\ \text{mm}^4
\]

\[
J={\pi r^4\over2}=1272345.02\ \text{mm}^4
\]

### Material

The selected material is **Aluminium 6061-T6**. This material is ductile, so the Von Mises and Tresca criteria are used.

| Property | Symbol | Value |
|---|---:|---:|
| Young's modulus | E | 68,900 MPa |
| Poisson's ratio | nu | 0.33 |
| Density | rho | 2700 kg/m^3 |
| Yield strength | S_y | 276 MPa |
| Ductility class | - | Ductile |

### Loading

| Load | Location | Direction | Magnitude |
|---|---|---|---:|
| Axial force | x = 600 mm | +x | 100 kN |
| Vertical transverse force | x = 600 mm | -y | 10 kN |
| Middle transverse force | x = 400 mm | +z | 20 kN |

The critical section is expected at the fixed end because the bending moments are maximum at the support.

---

## 2. Analytical Solution

### 2.1 Free Body Diagram and Support Reactions

The cantilever support at x = 0 must balance all external forces and bending moments.

Force equilibrium:

\[
\sum F_x=0:\quad R_x+100000=0
\]

\[
R_x=-100000\ \text{N}
\]

\[
\sum F_y=0:\quad R_y-10000=0
\]

\[
R_y=10000\ \text{N}
\]

\[
\sum F_z=0:\quad R_z+20000=0
\]

\[
R_z=-20000\ \text{N}
\]

Moment equilibrium about the fixed end:

\[
M_z=10000(600)=6000000\ \text{Nmm}
\]

\[
M_y=20000(400)=8000000\ \text{Nmm}
\]

The resultant bending moment at the fixed end is:

\[
M_R=\sqrt{M_y^2+M_z^2}
\]

\[
M_R=\sqrt{(8000000)^2+(6000000)^2}=10000000\ \text{Nmm}
\]

There is no externally applied torque about the x-axis in this idealized model:

\[
T=0
\]

### 2.2 Internal Loads at the Critical Section

At the fixed end:

| Internal resultant | Value |
|---|---:|
| Axial force, N | 100,000 N |
| Shear force in y, V_y | 10,000 N |
| Shear force in z, V_z | 20,000 N |
| Bending moment about z, M_z | 6,000,000 Nmm |
| Bending moment about y, M_y | 8,000,000 Nmm |
| Resultant bending moment, M_R | 10,000,000 Nmm |
| Torque, T | 0 Nmm |

The shear force and bending moment diagrams are piecewise:

For the y-direction load at the free end:

\[
V_y=-10000\ \text{N}\quad 0<x<600\ \text{mm}
\]

\[
M_z(x)=10000(600-x)\ \text{Nmm}
\]

For the z-direction point load at x = 400 mm:

\[
V_z=20000\ \text{N}\quad 0<x<400\ \text{mm}
\]

\[
V_z=0\quad 400<x<600\ \text{mm}
\]

\[
M_y(x)=20000(400-x)\ \text{Nmm}\quad 0<x<400\ \text{mm}
\]

\[
M_y(x)=0\quad 400<x<600\ \text{mm}
\]

### 2.3 Normal and Shear Stress

Axial normal stress:

\[
\sigma_a={N\over A}={100000\over2827.43}=35.37\ \text{MPa}
\]

Maximum bending normal stress:

\[
\sigma_b={M_Rc\over I}={10000000(30)\over636172.51}=471.57\ \text{MPa}
\]

Maximum combined tensile normal stress:

\[
\sigma_{max}=\sigma_a+\sigma_b=35.37+471.57=506.94\ \text{MPa}
\]

Maximum combined compressive normal stress:

\[
\sigma_{min}=\sigma_a-\sigma_b=35.37-471.57=-436.20\ \text{MPa}
\]

At the outer surface point where bending stress is maximum, the transverse shear stress from V_y and V_z is zero for a circular section boundary in elementary beam theory. Since T = 0, the torsional shear stress is also zero:

\[
\tau \approx 0\ \text{MPa}
\]

Therefore, the critical surface stress state is approximately uniaxial:

\[
\sigma_x=506.94\ \text{MPa},\quad \sigma_y=0,\quad \sigma_z=0,\quad \tau_{xy}=\tau_{xz}=\tau_{yz}=0
\]

### 2.4 Principal Stresses and Mohr's Circle

For the uniaxial critical stress state:

\[
\sigma_1=506.94\ \text{MPa}
\]

\[
\sigma_2=0\ \text{MPa}
\]

\[
\sigma_3=0\ \text{MPa}
\]

Maximum in-plane shear stress:

\[
\tau_{max,in-plane}={\sigma_1-\sigma_2\over2}=253.47\ \text{MPa}
\]

Maximum out-of-plane shear stress:

\[
\tau_{max}={\sigma_1-\sigma_3\over2}=253.47\ \text{MPa}
\]

### 2.5 Failure Theories

Because 6061-T6 aluminium is ductile, both Von Mises and Tresca criteria are evaluated.

Von Mises equivalent stress:

\[
\sigma_{VM}=\sqrt{\sigma_1^2+\sigma_2^2+\sigma_3^2-\sigma_1\sigma_2-\sigma_2\sigma_3-\sigma_3\sigma_1}
\]

\[
\sigma_{VM}=506.94\ \text{MPa}
\]

Tresca equivalent stress:

\[
\sigma_T=\max(|\sigma_1-\sigma_2|,\ |\sigma_2-\sigma_3|,\ |\sigma_1-\sigma_3|)
\]

\[
\sigma_T=506.94\ \text{MPa}
\]

Analytical factor of safety:

\[
n={S_y\over\sigma_{VM}}={276\over506.94}=0.54
\]

Since n < 1, the selected 60 mm diameter 6061-T6 aluminium shaft is not safe under the specified loading.

---

## 3. Computational Analysis: FEA

### 3.1 Model Setup

The finite element model was created using FreeCAD FEM and CalculiX. The automation script is saved as `shaft_6061_fem.py`, and the generated model is `shaft_6061_t6_fem.FCStd`.

Model properties:

| Item | Value |
|---|---|
| Geometry | Solid circular shaft |
| Length | 600 mm |
| Radius | 30 mm |
| Material | Aluminium 6061-T6 |
| Fixed support | Circular face at x = 0 |
| Axial load | 100 kN at x = 600 mm |
| End transverse load | 10 kN at x = 600 mm |
| Middle transverse load | 20 kN at x = 400 mm |
| Mesh tool | Gmsh |
| Mesh size | 3 mm minimum, 8 mm maximum |
| Solver | CalculiX |

The generated solver files are stored under `shaft_6061_fem_output/`.

### 3.2 Mesh

The mesh uses 3D solid elements. The input file contains 4041 nodes and 4048 volume elements. The mesh is refined enough for a first comparison, but additional local refinement should be applied near the fixed end because this is the maximum-stress region.

### 3.3 FEA Output Check

The original FreeCAD force export wrote incorrect total force magnitudes into the CalculiX `*CLOAD` blocks. This was corrected by normalizing each load block in `Gmsh_Mesh_3mm_8mm_corrected.inp` so that the total applied forces are exactly 100 kN, -10 kN, and 20 kN. The corrected model was solved directly with `ccx`. The extracted result summary is saved in `shaft_6061_fem_output/extracted_fea_values_corrected.txt`.

Extracted numerical result values:

| Quantity | Extracted FEA value |
|---|---:|
| Maximum displacement magnitude | 22.3217 mm |
| Node of maximum displacement | 113 |
| Coordinate of maximum displacement | x = 600.0 mm, y = 21.2132 mm, z = -21.2132 mm |
| Maximum Von Mises stress | 448.052 MPa |
| Node of maximum Von Mises stress | 790 |
| Coordinate of maximum Von Mises stress | x = 28.4394 mm, y = 18.4220 mm, z = -23.6776 mm |
| Maximum principal stress, sigma_1 | 640.058 MPa |
| Minimum principal stress, sigma_3 | -544.853 MPa |

FreeCAD screenshots exported by macro:

| Screenshot | File |
|---|---|
| Axometric model, mesh and loads | `freecad_screenshots/01_model_axometric.png` |
| Front view | `freecad_screenshots/02_model_front.png` |
| Top view | `freecad_screenshots/03_model_top.png` |
| Corrected Von Mises contour | `freecad_screenshots/04_corrected_von_mises.png` |
| Corrected sigma_1 contour | `freecad_screenshots/05_corrected_principal_sigma1.png` |
| Corrected sigma_3 contour | `freecad_screenshots/06_corrected_principal_sigma3.png` |
| Corrected displacement contour | `freecad_screenshots/07_corrected_displacement.png` |

The CalculiX reaction output file reports:

| Quantity | FEA output |
|---|---:|
| Total reaction F_x | -100,000 N |
| Total reaction F_y | 10,000 N |
| Total reaction F_z | -20,000 N |

The expected analytical support reactions are:

| Quantity | Expected analytical value |
|---|---:|
| R_x | -100,000 N |
| R_y | 10,000 N |
| R_z | -20,000 N |

After correction, the reaction forces match the analytical support reactions exactly. Therefore, the corrected CalculiX result is suitable for comparison with the hand calculation.

Required screenshots to insert into the final PDF:

1. CAD geometry and dimensions.
2. Fixed boundary condition at x = 0.
3. Applied loads at x = 600 mm and x = 400 mm.
4. Mesh plot.
5. Reaction force plot/table.
6. Normal stress distribution.
7. Shear stress distribution.
8. Principal stress plots, sigma_1, sigma_2, sigma_3.
9. Von Mises stress plot.
10. Probe result at the critical fixed-end outer surface point.

---

## 4. Results Comparison and Factor of Safety

The comparison below uses the corrected CalculiX input file. The FEA stress value selected for comparison is the maximum Von Mises stress away from the immediate fixed-face singularity. The fixed face itself shows a higher local principal stress because the ideal clamped boundary creates a stress concentration.

| Result | Analytical | FEA | Percent error |
|---|---:|---:|---:|
| R_x | -100,000 N | -100,000 N | 0.00% |
| R_y | 10,000 N | 10,000 N | 0.00% |
| R_z | -20,000 N | -20,000 N | 0.00% |
| Resultant bending moment | 10,000,000 Nmm | Implied by matching reactions | - |
| sigma_1 / nominal max stress | 506.94 MPa | 459.80 MPa at max-VM node | 9.30% |
| Von Mises stress | 506.94 MPa | 448.05 MPa | 11.62% |
| Tresca stress | 506.94 MPa | 457.35 MPa | 9.78% |
| Factor of safety | 0.54 | 0.62 | 13.14% |

The analytical and FEA stresses are close in order of magnitude. The difference is mainly due to the 3D solid model, discrete load application over faces, stress averaging at nodes, and local boundary effects near the clamped face.

---

## 5. Technical Discussion

The analytical solution predicts that the maximum stress occurs at the fixed end. This is expected for a cantilever beam because both transverse loads produce their largest bending moments at the built-in support. The axial force adds a uniform normal stress to the bending normal stress. At the critical outer surface point, the bending and axial stresses act in the same direction, giving a maximum tensile stress of 506.94 MPa.

The selected material, 6061-T6 aluminium, has a yield strength of approximately 276 MPa. The analytical Von Mises and Tresca stresses are both 506.94 MPa because the critical stress state is approximately uniaxial. This gives a factor of safety of 0.54, which is below 1.0. Therefore, yielding is expected, and the material/geometry combination is not acceptable for the assigned loading.

A safer design would require either a stronger material or a larger shaft diameter. Since bending stress varies with \(1/d^3\) for a solid circular shaft, increasing diameter is very effective. For example, keeping the same material and targeting n = 2 would require the maximum equivalent stress to be less than 138 MPa, so the diameter would need to be increased substantially.

The analytical model is based on classical beam theory. It assumes linear elastic behavior, small deflection, plane sections remaining plane, ideal point/resultant loads, and an ideal fixed support. It also neglects local 3D stress concentration near the load application regions and the fixed boundary. These assumptions are acceptable for estimating nominal stresses away from discontinuities, but they cannot capture local peaks caused by load patches, fixture edges, or mesh geometry.

FEA solves the 3D elasticity problem over the entire volume, so it can show stress gradients and local concentrations that are not present in the hand calculation. The first FreeCAD export wrote incorrect total concentrated-load magnitudes, so the `*CLOAD` blocks were normalized and the corrected input was solved again in CalculiX. The corrected reaction forces match the analytical reactions exactly, confirming that the load equilibrium is now correct.

Mesh density also affects the comparison. A coarse mesh can underpredict bending stress because the stress gradient across the section is not represented accurately. Near a fixed support, very fine meshes may produce increasing local peak stress due to the idealized boundary condition. For comparison with beam theory, the best practice is to probe stresses slightly away from the fixed face, at a distance where Saint-Venant effects have decayed, while still close enough to represent the critical section.

---

## 6. Conclusion

The analytical combined-loading calculation gives a maximum tensile normal stress and Von Mises stress of **506.94 MPa** at the fixed-end outer surface. For 6061-T6 aluminium with \(S_y=276\ \text{MPa}\), the factor of safety is:

\[
n=0.54
\]

Thus, the current design is **not structurally safe** under the assigned loading. The shaft should be redesigned using a larger diameter and/or a higher-strength material.

The corrected FEA solution gives a maximum nominal Von Mises stress of **448.05 MPa** and a corresponding FEA factor of safety of **0.62**. Both analytical and FEA results show that the current shaft is unsafe.

---

## Appendix A: Files Used

| File | Purpose |
|---|---|
| `MECT2222_Project.pdf` | Project instructions and rubric |
| `MECT2222_Project Assignment Sheet.pdf` | Assignment sheet |
| `shaft_6061_fem.py` | FreeCAD FEM automation script |
| `shaft_6061_t6_fem.FCStd` | Generated FreeCAD model |
| `shaft_6061_fem_output/Gmsh_Mesh_3mm_8mm.inp` | CalculiX input file |
| `shaft_6061_fem_output/Gmsh_Mesh_3mm_8mm.dat` | CalculiX reaction-force output |
| `shaft_6061_fem_output/Gmsh_Mesh_3mm_8mm.frd` | CalculiX result file |
| `shaft_6061_fem_output/Gmsh_Mesh_3mm_8mm_corrected.inp` | Corrected CalculiX input file |
| `shaft_6061_fem_output/Gmsh_Mesh_3mm_8mm_corrected.dat` | Corrected reaction-force output |
| `shaft_6061_fem_output/Gmsh_Mesh_3mm_8mm_corrected.frd` | Corrected FEA result file |
| `freecad_screenshots/*.png` | FreeCAD screenshots and corrected result plots |
