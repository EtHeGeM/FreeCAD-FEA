import os
from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui


ROOT = Path("/home/eren/Belgeler/eng-mechanics")
MODEL = ROOT / "shaft_6061_t6_fem.FCStd"
OUT_DIR = ROOT / "freecad_screenshots"
OUT_DIR.mkdir(exist_ok=True)


def save_view(name, view_fn):
    view = Gui.ActiveDocument.ActiveView
    view_fn(view)
    view.fitAll()
    Gui.updateGui()
    view.saveImage(str(OUT_DIR / name), 1800, 1200, "White")


doc = App.openDocument(str(MODEL))
Gui.ActiveDocument = Gui.getDocument(doc.Name)

for obj in doc.Objects:
    try:
        obj.ViewObject.Visibility = obj.Name in {
            "Partitioned_Shaft",
            "Gmsh_Mesh_3mm_8mm",
            "Fixed_End_x0",
            "End_Axial_100kN_plus_X",
            "End_Vertical_10kN_minus_Y",
            "Middle_20kN_plus_Z",
        }
    except Exception:
        pass

save_view("01_model_axometric.png", lambda view: view.viewAxometric())
save_view("02_model_front.png", lambda view: view.viewFront())
save_view("03_model_top.png", lambda view: view.viewTop())

print(f"Saved screenshots to: {OUT_DIR}")

try:
    from PySide import QtCore, QtGui

    QtCore.QTimer.singleShot(500, QtGui.QApplication.instance().quit)
except Exception:
    pass
