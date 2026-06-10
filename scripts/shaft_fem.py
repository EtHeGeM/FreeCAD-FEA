import FreeCAD
import Part
import ObjectsFem
import os

doc = FreeCAD.newDocument("shaft_6061_t6_fem")

# --------------------------------------------------
# Geometry
# --------------------------------------------------
L = 400.0      # mm
r = 30.0       # mm

shaft_shape = Part.makeCylinder(
    r,
    L,
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(1, 0, 0)
)

shaft = doc.addObject("Part::Feature", "Solid_Cylinder")
shaft.Shape = shaft_shape
doc.recompute()

# Print face centers to verify Face names
print("Faces:")
for i, face in enumerate(shaft.Shape.Faces, start=1):
    c = face.CenterOfMass
    print(f"Face{i}: center = ({c.x:.3f}, {c.y:.3f}, {c.z:.3f})")

# --------------------------------------------------
# FEM Analysis
# --------------------------------------------------
analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

# --------------------------------------------------
# Material: Aluminium 6061-T6
# --------------------------------------------------
mat = ObjectsFem.makeMaterialSolid(doc, "Aluminium_6061_T6")
mat.Material = {
    "Name": "Aluminium 6061-T6",
    "YoungsModulus": "68900 MPa",
    "PoissonRatio": "0.33",
    "Density": "2700 kg/m^3"
}
analysis.addObject(mat)

# --------------------------------------------------
# Boundary condition: fixed right end
# You MUST verify Face number from printed output.
# Usually:
# Face1 or Face2 = end caps
# Face3 = cylindrical outer face
# --------------------------------------------------

# Default assumption:
# Face at x = 400 mm is right end.
right_face_name = None
left_face_name = None

for i, face in enumerate(shaft.Shape.Faces, start=1):
    c = face.CenterOfMass
    if abs(c.x - L) < 1e-6:
        right_face_name = f"Face{i}"
    if abs(c.x - 0.0) < 1e-6:
        left_face_name = f"Face{i}"

print("Left face:", left_face_name)
print("Right face:", right_face_name)

fixed = ObjectsFem.makeConstraintFixed(doc, "Fixed_Right_End")
fixed.References = [(shaft, right_face_name)]
analysis.addObject(fixed)

# --------------------------------------------------
# Loads
# --------------------------------------------------
# FreeCAD FEM force direction scripting can be sensitive.
# We create force objects referencing the left face.
# Direction may require adjustment depending on FreeCAD version.

force_axial = ObjectsFem.makeConstraintForce(doc, "Left_Axial_100kN")
force_axial.References = [(shaft, left_face_name)]
force_axial.Force = 100000.0
force_axial.Reversed = True
analysis.addObject(force_axial)

force_vertical = ObjectsFem.makeConstraintForce(doc, "Left_Vertical_10kN")
force_vertical.References = [(shaft, left_face_name)]
force_vertical.Force = 10000.0
force_vertical.Reversed = True
analysis.addObject(force_vertical)

# --------------------------------------------------
# Mesh with Gmsh
# --------------------------------------------------
mesh = ObjectsFem.makeMeshGmsh(doc, "FEMMeshGmsh")
mesh.Part = shaft
mesh.CharacteristicLengthMax = 8.0
mesh.CharacteristicLengthMin = 3.0
analysis.addObject(mesh)

# --------------------------------------------------
# Solver: CalculiX
# --------------------------------------------------
solver = ObjectsFem.makeSolverCalculixCcxTools(doc, "CalculiX")
analysis.addObject(solver)

doc.recompute()

# --------------------------------------------------
# Save model
# --------------------------------------------------
output_path = os.path.expanduser("~/shaft_6061_t6_fem.FCStd")
doc.saveAs(output_path)

print("Model saved to:", output_path)
print("Open this file with FreeCAD GUI to inspect constraints and mesh.")