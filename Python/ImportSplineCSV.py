#Author-Autodesk Inc
#Description-Import spline from csv file

import adsk.core, adsk.fusion, traceback

def main():
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # Get all components in the active design.
        product = app.activeProduct
        design = product
        title = 'Import Spline csv'
        if not design:
            ui.messageBox('No active Fusion design', title)
            return
        
        dlg = ui.createFileDialog()
        dlg.title = 'Open CSV File'
        dlg.filter = 'Comma Separated Values (*.csv);;All Files (*.*)'
        if dlg.showOpen() != adsk.core.DialogResults.DialogOK :
            return

        filename = dlg.filename
        # Try opening the file with a different encoding
        with open(filename, 'r', encoding='ISO-8859-1') as f:
            points = adsk.core.ObjectCollection.create()
            for line in f:
                pntStrArr = line.strip().split(',')
                if len(pntStrArr) >= 3:
                    points.add(adsk.core.Point3D.create(float(pntStrArr[0]), float(pntStrArr[1]), float(pntStrArr[2])))       
        root = design.rootComponent;
        sketch = root.sketches.add(root.xYConstructionPlane);
        sketch.sketchCurves.sketchFittedSplines.add(points);     
    except Exception as e:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
main()
