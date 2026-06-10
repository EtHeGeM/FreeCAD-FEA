#!/usr/bin/env python3
"""
Terminal FreeCAD FEM automation for a 6061-T6 aluminium cantilever shaft.

Run with:
    FreeCADCmd shaft_6061_fem.py
    freecadcmd shaft_6061_fem.py

The script creates a partitioned cylindrical shaft so that the x = 400 mm
interface is addressable for the middle transverse load. It then creates FEM
objects, attempts Gmsh meshing and CalculiX solving, saves the FreeCAD model,
and prints engineering sanity-check values.
"""

from __future__ import annotations

import math
import shutil
import sys
import traceback
from pathlib import Path


LENGTH_MM = 600.0
RADIUS_MM = 30.0
MID_X_MM = 400.0
FIXED_X_MM = 0.0
FREE_END_X_MM = LENGTH_MM

E_MPA = 68900.0
NU = 0.33
DENSITY = "2700 kg/m^3"
YIELD_MPA = 276.0

END_AXIAL_N = 100000.0
END_VERTICAL_N = -10000.0
MIDDLE_TRANSVERSE_N = 20000.0

END_AXIAL_POINT = (FREE_END_X_MM, 0.0, -RADIUS_MM)
END_VERTICAL_POINT = (FREE_END_X_MM, 0.0, RADIUS_MM)
MIDDLE_TRANSVERSE_POINT = (MID_X_MM, RADIUS_MM, 0.0)

MESH_MAX_MM = 8.0
MESH_MIN_MM = 3.0
FORCE_ARROW_LENGTH_MM = 80.0

OUT_DIR = Path.cwd() / "shaft_6061_fem_output"
FCSTD_PATH = Path.cwd() / "shaft_6061_t6_fem.FCStd"

TOL = 1.0e-5


def die(message: str, exit_code: int = 1) -> None:
    print(f"\nERROR: {message}")
    sys.exit(exit_code)


def import_freecad_modules():
    try:
        import FreeCAD  # type: ignore
        import Part  # type: ignore
        import ObjectsFem  # type: ignore
        import Fem  # type: ignore  # noqa: F401
    except ImportError as exc:
        die(
            "FreeCAD FEM Python modules are missing or this script was not run "
            "with FreeCADCmd/freecadcmd.\n"
            f"Import error: {exc}\n"
            "Install FreeCAD with FEM support, then run: FreeCADCmd shaft_6061_fem.py"
        )
    return FreeCAD, Part, ObjectsFem


def executable_status(name: str, install_hint: str) -> bool:
    path = shutil.which(name)
    if path:
        print(f"Found {name}: {path}")
        return True
    print(f"WARNING: {name} executable not found. {install_hint}")
    return False


def face_center(face):
    c = face.CenterOfMass
    return c.x, c.y, c.z


def print_faces(shape) -> list[tuple[str, object, tuple[float, float, float], float]]:
    print("\nDetected shape faces:")
    rows = []
    for index, face in enumerate(shape.Faces, start=1):
        name = f"Face{index}"
        center = face_center(face)
        rows.append((name, face, center, face.Area))
        print(
            f"  {name:>6s}: center=({center[0]:9.4f}, {center[1]:9.4f}, "
            f"{center[2]:9.4f}) mm, area={face.Area:12.4f} mm^2"
        )
    return rows


def find_planar_circular_faces(rows, x_mm: float, label: str) -> list[str]:
    expected_area = math.pi * RADIUS_MM**2
    matches = []
    for name, face, center, area in rows:
        if abs(center[0] - x_mm) <= TOL and abs(area - expected_area) / expected_area < 1.0e-3:
            matches.append(name)
    if not matches:
        die(
            f"Could not detect {label} face at x = {x_mm:g} mm. "
            "Check printed face centers and geometry creation."
        )
    return matches


def set_existing_property(obj, candidates, value) -> bool:
    props = set(obj.PropertiesList)
    for prop in candidates:
        if prop in props:
            try:
                setattr(obj, prop, value)
                return True
            except Exception:
                pass
    return False


def set_mesh_part(mesh, shaft) -> bool:
    """Attach the geometry to a Gmsh mesh object across FreeCAD versions."""
    props = set(getattr(mesh, "PropertiesList", []))
    for prop, value in (
        ("Part", shaft),
        ("Shape", shaft),
        ("Geometry", shaft),
        ("Base", shaft),
    ):
        if prop in props:
            try:
                setattr(mesh, prop, value)
                return True
            except Exception:
                pass

    for prop, value in (
        ("References", [(shaft, "")]),
        ("BaseFeature", [(shaft, "")]),
    ):
        if prop in props:
            try:
                setattr(mesh, prop, value)
                return True
            except Exception:
                pass

    print("WARNING: Could not attach geometry to Gmsh mesh object automatically.")
    print(f"Gmsh mesh properties available: {', '.join(sorted(props))}")
    return False


def set_mesh_sizes(mesh) -> None:
    """Set Gmsh mesh sizing while tolerating FreeCAD API name changes."""
    if not set_existing_property(
        mesh,
        ["CharacteristicLengthMax", "MaxSize", "ElementDimensionMax", "MeshSizeMax"],
        MESH_MAX_MM,
    ):
        print("WARNING: Could not set maximum Gmsh element size on this FreeCAD version.")

    if not set_existing_property(
        mesh,
        ["CharacteristicLengthMin", "MinSize", "ElementDimensionMin", "MeshSizeMin"],
        MESH_MIN_MM,
    ):
        print("WARNING: Could not set minimum Gmsh element size on this FreeCAD version.")


def make_calculix_solver(doc, ObjectsFem):
    """Create a CalculiX solver object across FreeCAD naming variants."""
    for factory_name in (
        "makeSolverCalculixCcxTools",
        "makeSolverCalculiXCcxTools",
        "makeSolverCalculix",
    ):
        factory = getattr(ObjectsFem, factory_name, None)
        if factory is None:
            continue
        try:
            solver = factory(doc, "CalculiX_Static")
            print(f"Created CalculiX solver with ObjectsFem.{factory_name}")
            return solver
        except Exception:
            pass

    available = [name for name in dir(ObjectsFem) if "Solver" in name or "Calcul" in name]
    die(
        "Could not create a CalculiX solver object with this FreeCAD API.\n"
        f"Available ObjectsFem solver-related names: {', '.join(sorted(available))}"
    )


def make_direction_edge(doc, FreeCAD, Part, name: str, start_point, unit_vec, visible: bool):
    start = FreeCAD.Vector(*(start_point or (0.0, 0.0, 0.0)))
    end = start + FreeCAD.Vector(
        unit_vec.x * FORCE_ARROW_LENGTH_MM,
        unit_vec.y * FORCE_ARROW_LENGTH_MM,
        unit_vec.z * FORCE_ARROW_LENGTH_MM,
    )
    edge = doc.addObject("Part::Feature", name)
    edge.Shape = Part.makeLine(start, end)
    edge.Label = name.replace("_", " ")
    edge.Visibility = visible
    try:
        edge.ViewObject.LineWidth = 4
        edge.ViewObject.PointSize = 6
        edge.ViewObject.LineColor = (1.0, 0.0, 0.0)
    except Exception:
        pass
    print(
        f"  Direction helper {name}: start=({start.x:g}, {start.y:g}, {start.z:g}) "
        f"end=({end.x:g}, {end.y:g}, {end.z:g})"
    )
    return edge


def configure_force_vector(force_obj, FreeCAD, Part, doc, vector, magnitude: float, start_point=None) -> None:
    """Configure a FreeCAD Fem::ConstraintForce across common API variants."""
    force_obj.Force = float(abs(magnitude))

    vec = FreeCAD.Vector(*vector)
    if vec.Length == 0:
        die(f"Zero load vector requested for {force_obj.Name}.")
    unit_vec = FreeCAD.Vector(vec)
    unit_vec.normalize()

    configured = False
    if "Direction" in set(force_obj.PropertiesList):
        try:
            direction_edge = make_direction_edge(
                doc,
                FreeCAD,
                Part,
                f"{force_obj.Name}_Requested_Direction",
                start_point,
                unit_vec,
                True,
            )
            force_obj.Direction = (direction_edge, ["Edge1"])
            configured = True
        except Exception:
            pass

    configured |= set_existing_property(force_obj, ["DirectionVector", "Vector"], unit_vec)
    configured |= set_existing_property(force_obj, ["ForceVector"], vec)

    # Older FreeCAD releases often use DirectionMode plus Reversed. Keep these
    # assignments opportunistic because property names changed across releases.
    for mode in ("Custom", "User-defined vector", "Vector"):
        if set_existing_property(force_obj, ["DirectionMode"], mode):
            break
    set_existing_property(force_obj, ["Reversed"], False)

    if not configured:
        print(
            f"WARNING: Could not find a direct vector property on {force_obj.Name}. "
            "The load object was created, but verify its direction in FreeCAD. "
            f"Requested vector: ({vector[0]}, {vector[1]}, {vector[2]}) N."
        )


def add_force(
    doc,
    analysis,
    ObjectsFem,
    FreeCAD,
    Part,
    name: str,
    part_obj,
    face_names: list[str],
    vector,
    start_point=None,
) -> object:
    force = ObjectsFem.makeConstraintForce(doc, name)
    force.References = [(part_obj, face_name) for face_name in face_names]
    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    configure_force_vector(force, FreeCAD, Part, doc, vector, magnitude, start_point=start_point)
    analysis.addObject(force)
    return force


def make_geometry(doc, FreeCAD, Part):
    # A compound of two touching solids preserves addressable faces at x = 400 mm
    # while still representing one continuous shaft for meshing/solving.
    left = Part.makeCylinder(
        RADIUS_MM,
        MID_X_MM,
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(1, 0, 0),
    )
    right = Part.makeCylinder(
        RADIUS_MM,
        LENGTH_MM - MID_X_MM,
        FreeCAD.Vector(MID_X_MM, 0, 0),
        FreeCAD.Vector(1, 0, 0),
    )
    compound = Part.makeCompound([left, right])
    shaft = doc.addObject("Part::Feature", "Partitioned_Shaft")
    shaft.Shape = compound
    doc.recompute()
    return shaft


def create_mesh(doc, analysis, ObjectsFem, shaft):
    mesh = ObjectsFem.makeMeshGmsh(doc, "Gmsh_Mesh_3mm_8mm")
    set_mesh_part(mesh, shaft)
    set_mesh_sizes(mesh)
    analysis.addObject(mesh)
    doc.recompute()

    try:
        from femmesh.gmshtools import GmshTools  # type: ignore

        print("\nCreating FEM mesh with Gmsh...")
        gmsh = GmshTools(mesh)
        error = gmsh.create_mesh()
        if error:
            print(f"WARNING: Gmsh returned: {error}")
        doc.recompute()
        if getattr(mesh, "FemMesh", None) and mesh.FemMesh.NodeCount:
            print(f"Mesh status: {mesh.FemMesh.NodeCount} nodes, {mesh.FemMesh.VolumeCount} volume elements")
        else:
            print("WARNING: Mesh object was created, but no FEM mesh data was found.")
    except Exception as exc:
        print("WARNING: Automatic Gmsh meshing failed.")
        print(f"Reason: {exc}")
        print("Install/check Gmsh, for example: sudo apt install gmsh")
    return mesh


def solve_with_calculix(doc, analysis, solver) -> tuple[str, object | None]:
    OUT_DIR.mkdir(exist_ok=True)
    try:
        from femtools import ccxtools  # type: ignore

        print("\nRunning CalculiX through FreeCAD femtools.ccxtools...")
        fea = ccxtools.FemToolsCcx(analysis)
        fea.update_objects()
        fea.setup_working_dir(str(OUT_DIR))
        fea.setup_ccx()
        fea.write_inp_file()
        inp = getattr(fea, "inp_file_name", None)
        if inp:
            print(f"CalculiX input file: {inp}")
        fea.ccx_run()
        fea.load_results()
        doc.recompute()
        return "solved", getattr(fea, "results", None)
    except Exception as exc:
        print("WARNING: Automatic CalculiX solve failed.")
        print(f"Reason: {exc}")
        print("Install/check CalculiX, for example: sudo apt install calculix-ccx")
        return "not solved", None


def export_results(doc) -> tuple[float | None, float | None]:
    max_disp = None
    max_mises = None

    for obj in doc.Objects:
        props = set(getattr(obj, "PropertiesList", []))
        if "Stats" in props:
            try:
                stats = obj.Stats
                print(f"Result stats from {obj.Name}: {stats}")
            except Exception:
                pass
        for prop in ("DisplacementLengths", "Displacement"):
            if prop in props:
                try:
                    values = list(getattr(obj, prop))
                    if values:
                        max_disp = max(max_disp or 0.0, max(float(v) for v in values))
                except Exception:
                    pass
        for prop in ("StressValues", "vonMises", "VonMises"):
            if prop in props:
                try:
                    values = list(getattr(obj, prop))
                    if values:
                        max_mises = max(max_mises or 0.0, max(float(v) for v in values))
                except Exception:
                    pass

    try:
        import importVTKResults  # type: ignore

        for obj in doc.Objects:
            if "Fem::FemResultObject" in getattr(obj, "TypeId", ""):
                vtk_path = OUT_DIR / f"{obj.Name}.vtu"
                importVTKResults.export([obj], str(vtk_path))
                print(f"Exported VTU result: {vtk_path}")
    except Exception as exc:
        print(f"VTU export skipped: {exc}")

    return max_disp, max_mises


def print_theory_reference() -> None:
    area = math.pi * RADIUS_MM**2
    inertia = math.pi * RADIUS_MM**4 / 4.0
    axial_stress_100 = abs(END_AXIAL_N) / area
    moment_from_10kn = abs(END_VERTICAL_N) * (END_VERTICAL_POINT[0] - FIXED_X_MM)
    moment_from_20kn = abs(MIDDLE_TRANSVERSE_N) * (MIDDLE_TRANSVERSE_POINT[0] - FIXED_X_MM)
    resultant_bending_moment = math.sqrt(moment_from_10kn**2 + moment_from_20kn**2)
    bending_stress = resultant_bending_moment * RADIUS_MM / inertia
    combined_simple = axial_stress_100 + bending_stress

    print("\nBeam-theory sanity check:")
    print(f"  Cross-sectional area A       = {area:.3f} mm^2")
    print(f"  Second moment of area I      = {inertia:.3f} mm^4")
    print(f"  Axial stress from 100 kN     = {axial_stress_100:.3f} MPa")
    print(f"  Moment from 10 kN at x=600   = {moment_from_10kn:.3f} N*mm")
    print(f"  Moment from 20 kN at x=400   = {moment_from_20kn:.3f} N*mm")
    print(f"  Resultant bending stress     = {bending_stress:.3f} MPa")
    print(f"  Simple combined stress ref.  = {combined_simple:.3f} MPa")
    print(f"  Expected critical region     = near fixed end at x = {FIXED_X_MM:g} mm")


def main() -> None:
    FreeCAD, Part, ObjectsFem = import_freecad_modules()

    print("FreeCAD FEM shaft automation")
    print(f"Output directory: {OUT_DIR}")
    executable_status("gmsh", "Install with: sudo apt install gmsh")
    executable_status("ccx", "Install with: sudo apt install calculix-ccx")

    doc = FreeCAD.newDocument("shaft_6061_t6_fem")
    shaft = make_geometry(doc, FreeCAD, Part)
    face_rows = print_faces(shaft.Shape)

    fixed_faces = find_planar_circular_faces(face_rows, FIXED_X_MM, "fixed end")
    free_end_faces = find_planar_circular_faces(face_rows, FREE_END_X_MM, "free end")
    middle_faces = find_planar_circular_faces(face_rows, MID_X_MM, "middle loading/interface")
    middle_load_faces = [middle_faces[0]]
    if len(middle_faces) > 1:
        print(
            "Middle interface has coincident partition faces; applying the 20 kN "
            f"load to {middle_load_faces[0]} and leaving the paired face unloaded."
        )

    analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

    material = ObjectsFem.makeMaterialSolid(doc, "Aluminium_6061_T6")
    material.Material = {
        "Name": "Aluminium 6061-T6",
        "YoungsModulus": f"{E_MPA:g} MPa",
        "PoissonRatio": f"{NU:g}",
        "Density": DENSITY,
    }
    analysis.addObject(material)

    fixed = ObjectsFem.makeConstraintFixed(doc, "Fixed_End_x0")
    fixed.References = [(shaft, face_name) for face_name in fixed_faces]
    analysis.addObject(fixed)

    add_force(
        doc,
        analysis,
        ObjectsFem,
        FreeCAD,
        Part,
        "End_Axial_100kN_plus_X",
        shaft,
        free_end_faces,
        (END_AXIAL_N, 0.0, 0.0),
        start_point=END_AXIAL_POINT,
    )
    add_force(
        doc,
        analysis,
        ObjectsFem,
        FreeCAD,
        Part,
        "End_Vertical_10kN_minus_Y",
        shaft,
        free_end_faces,
        (0.0, END_VERTICAL_N, 0.0),
        start_point=END_VERTICAL_POINT,
    )
    add_force(
        doc,
        analysis,
        ObjectsFem,
        FreeCAD,
        Part,
        "Middle_20kN_plus_Z",
        shaft,
        middle_load_faces,
        (0.0, 0.0, MIDDLE_TRANSVERSE_N),
        start_point=MIDDLE_TRANSVERSE_POINT,
    )

    mesh = create_mesh(doc, analysis, ObjectsFem, shaft)
    solver = make_calculix_solver(doc, ObjectsFem)
    analysis.addObject(solver)
    doc.recompute()

    solver_status = solve_with_calculix(doc, analysis, solver)
    max_disp, max_mises = export_results(doc)

    doc.saveAs(str(FCSTD_PATH))

    print("\nSummary:")
    print(f"  Geometry                  = cylinder, L={LENGTH_MM:g} mm, r={RADIUS_MM:g} mm, axis=X")
    print(f"  Material                  = Aluminium 6061-T6, E={E_MPA:g} MPa, nu={NU:g}, rho={DENSITY}")
    print(f"  Yield strength reference  = {YIELD_MPA:g} MPa")
    print(f"  Fixed face(s), x=0        = {', '.join(fixed_faces)}")
    print(f"  Free end face(s), x=600   = {', '.join(free_end_faces)}")
    print(f"  Middle detected face(s)   = {', '.join(middle_faces)}")
    print(f"  Middle loaded face        = {', '.join(middle_load_faces)}")
    print(f"  100 kN force point/vector = {END_AXIAL_POINT}, ({END_AXIAL_N:g}, 0, 0) N")
    print(f"  20 kN force point/vector  = {MIDDLE_TRANSVERSE_POINT}, (0, 0, {MIDDLE_TRANSVERSE_N:g}) N")
    print(f"  10 kN force point/vector  = {END_VERTICAL_POINT}, (0, {END_VERTICAL_N:g}, 0) N")
    if getattr(mesh, "FemMesh", None) and mesh.FemMesh.NodeCount:
        print(f"  Mesh status               = {mesh.FemMesh.NodeCount} nodes, {mesh.FemMesh.VolumeCount} volume elements")
    else:
        print("  Mesh status               = mesh not generated or unavailable")
    print(f"  Solver status             = {solver_status[0]}")
    print(f"  Saved FreeCAD model       = {FCSTD_PATH}")
    print(f"  Solver/output directory   = {OUT_DIR}")
    if max_disp is not None:
        print(f"  Maximum displacement      = {max_disp:.6g} mm")
    else:
        print("  Maximum displacement      = unavailable")
    if max_mises is not None:
        fos = YIELD_MPA / max_mises if max_mises > 0 else math.inf
        print(f"  Maximum von Mises stress  = {max_mises:.6g} MPa")
        print(f"  Factor of safety          = {fos:.4g}")
    else:
        print("  Maximum von Mises stress  = unavailable")

    print_theory_reference()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        die("Unexpected failure. Review the traceback above and the printed face/debug information.")
