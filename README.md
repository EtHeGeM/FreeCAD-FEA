# FreeCAD FEA - MECT2222 Combined Loading Project

This repository contains the FreeCAD/CalculiX finite element model, analytical report, corrected solver input/output, screenshots, and helper scripts for the MECT2222 combined-loading and FEA validation project.

## Main Report

- `reports/MECT2222_Project_Report.pdf`
- `reports/MECT2222_Project_Report.tex`
- `reports/MECT2222_Project_Report.md`

## FreeCAD/FEA Files

- `models/shaft_6061_t6_fem.FCStd` - FreeCAD FEM model
- `scripts/shaft_6061_fem.py` - FreeCAD FEM automation script
- `fea_output/Gmsh_Mesh_3mm_8mm_corrected.inp` - corrected CalculiX input file
- `fea_output/Gmsh_Mesh_3mm_8mm_corrected.dat` - corrected reaction-force output
- `fea_output/Gmsh_Mesh_3mm_8mm_corrected.frd` - corrected result file
- `fea_output/extracted_fea_values_corrected.txt` - parsed FEA values

## Utility Scripts

- `scripts/fix_and_run_calculix.py` - normalizes FreeCAD CLOAD totals and reruns CalculiX
- `scripts/extract_fea_values.py` - parses FRD/DAT output for displacement and stress values
- `scripts/export_freecad_screenshots.py` - exports FreeCAD model screenshots
- `scripts/plot_corrected_fea_results.py` - creates stress/displacement result plots

## Figures

- `figures/freecad_screenshots/` - FreeCAD model views and corrected FEA contour plots

## Source Documents

- `source_docs/MECT2222_Project.pdf`
- `source_docs/MECT2222_Project Assignment Sheet.pdf`

## Final Exam Study Notes

The `study_notes/final_exam/` directory contains the graphical final-exam solution notes created from `FINAL_Exercise_Questions.pdf`.

## Reproduce Corrected CalculiX Run

```bash
python3 scripts/fix_and_run_calculix.py
python3 scripts/extract_fea_values.py
python3 scripts/plot_corrected_fea_results.py
```

Requirements:

- FreeCAD with FEM workbench
- Gmsh
- CalculiX (`ccx`)
- Python 3 with matplotlib and Pillow for plotting/cropping utilities
