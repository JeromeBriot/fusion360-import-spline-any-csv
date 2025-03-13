#Author-Jerome Briot (inpired by the ImportSplineCSV script from Autodesk)
#Description-Import spline from any CSV file
#Version-1.5.0

import adsk.core, adsk.fusion, traceback
import io

VERBOSE = True

TREAT_EMPTY_LINES_AS_SPLINES_SEPARATOR = True

ONE_SKETCH_PER_SPLINE = False

SCALE_FACTOR = 1.0

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # Get all components in the active design.
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        root = design.rootComponent

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

            splines = []
            
            splines.append(adsk.core.ObjectCollection.create())

            data = []

            for line in f:

                line = line.rstrip()

                if line == '' or len(line) < 3:

                    if TREAT_EMPTY_LINES_AS_SPLINES_SEPARATOR:

                        if len(splines[-1]) == 0:
                            splines.pop()
                        splines.append(adsk.core.ObjectCollection.create())

                else:

                    # Skip header if any
                    if not(line[0]=='-' or line[0]=='+' or line[0].isdigit()):
                        continue

                    # Get all decimal and value separators
                    separators = [x for x in line if x not in ['+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'E', 'e', 'D', 'd']]

                    # If only one separator then no decimal separator (e.g. line contains 5,0)
                    if all([x == separators[0] for x in separators]):
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
                            data.append(float(pntStr) * SCALE_FACTOR)
                        except:
                            break

                    if len(data) >= 3 :
                        point = adsk.core.Point3D.create(data[0], data[1], data[2])
                        splines[-1].add(point)

                    data.clear()

        if len(splines[-1]) == 0:
            splines.pop()

        if ONE_SKETCH_PER_SPLINE:
            for spline in splines:
                if len(spline) > 0:
                    sketch = root.sketches.add(root.xYConstructionPlane)
                    sketch.sketchCurves.sketchFittedSplines.add(spline)
        else:
            sketch = root.sketches.add(root.xYConstructionPlane)
            for spline in splines:
                if len(spline) > 0:                    
                    sketch.sketchCurves.sketchFittedSplines.add(spline)

        if VERBOSE:

            if len(splines) == 0:
                message = 'No spline imported.'
                icon = adsk.core.MessageBoxIconTypes.WarningIconType
            elif len(splines) == 1:
                message = 'One spline imported.'
                icon = adsk.core.MessageBoxIconTypes.InformationIconType
            else:
                message = f'{len(splines)} splines imported.'
                icon = adsk.core.MessageBoxIconTypes.InformationIconType

            ui.messageBox(message, title, adsk.core.MessageBoxButtonTypes.OKButtonType, icon)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
