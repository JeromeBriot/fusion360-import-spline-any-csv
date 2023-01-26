#Author-Jerome Briot (inpired by the ImportSplineCSV script from Autodesk)
#Description-Import spline from any CSV file
#Version-1.0.0

import adsk.core, adsk.fusion, traceback
import io

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # Get all components in the active design.
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        title = 'Import Spline From Any CSV'
        if not design:
            ui.messageBox('No active Fusion design', title)
            return

        dlg = ui.createFileDialog()
        dlg.title = 'Open CSV File'
        dlg.filter = 'Comma Separated Values (*.csv);;All Files (*.*)'
        if dlg.showOpen() != adsk.core.DialogResults.DialogOK :
            return

        filename = dlg.filename
        with io.open(filename, 'r', encoding='utf-8-sig') as f:
            points = adsk.core.ObjectCollection.create()
            line = f.readline().strip()

            data = []
            while line:

                # Skip header if any
                if not(line[0]=='-' or line[0]=='+' or line[0].isdigit()):
                    line = f.readline().strip()
                    continue

                # Get all decimal and value separators
                separators = [x for x in line if x not in ['+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'E', 'e', 'D', 'd']]

                # If only one separator then no decimal separator (e.g. line contains 5,0)
                if len(separators) == 1:
                    valueSep = separators[0]
                    decimalSep = ''
                else:
                    # The list contains alternate separators (e.g. ['.', ';', '.', ';', '.'])
                    # decimalSep is the first one and valueSep is the second one
                    decimalSep = separators[0]
                    valueSep = separators[1]

                # If the decimal separator is a comma then replace it by a period
                if decimalSep == ',':
                    line = line.replace(',', '.')

                pntStrArr = line.split(valueSep)

                # If only two columns then add a third one (i.e. Z = 0.0)
                if len(pntStrArr) < 3:
                    pntStrArr.append('0.0')
                # If three columns but the 3rd one is empty then set it to 0.0
                elif len(pntStrArr) == 3 and pntStrArr[-1] == '':
                    pntStrArr[-1] = '0.0'
                elif len(pntStrArr) > 3:
                    # Else if more than three columns then skip this iteration  (i.e. no point created)
                    break

                for pntStr in pntStrArr:
                    try:
                        data.append(float(pntStr))
                    except:
                        break

                if len(data) >= 3 :
                    point = adsk.core.Point3D.create(data[0], data[1], data[2])
                    points.add(point)
                line = f.readline().strip()
                data.clear()
        if points.count:
            root = design.rootComponent
            sketch = root.sketches.add(root.xYConstructionPlane)
            sketch.sketchCurves.sketchFittedSplines.add(points)
        else:
            ui.messageBox('No valid points', title)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
