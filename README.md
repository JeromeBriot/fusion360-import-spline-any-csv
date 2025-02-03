# ImportSplineAnyCSV for Fusion 360
A Fusion 360 script that import spline from any CSV file.

It reads data from a CSV file and creates a spline in a sketch. It supports:

- two colunms and three columns data
- numbers with a comma as the decimal separator
- any kind of separator between values
- automatic text header skipping

Since the version 1.2.0, it is possible to import multiple splines from one CSV file by separate them with empty lines.
You have to edit the file ImportSplineAnyCSV.py with a text editor and set the TREAT_EMPTY_LINES_AS_SPLINES_SEPARATOR variable to True:

```TREAT_EMPTY_LINES_AS_SPLINES_SEPARATOR = True```

If you want to import data as one spline only, you have to set the TREAT_EMPTY_LINES_AS_SPLINES_SEPARATOR variable to False:

```TREAT_EMPTY_LINES_AS_SPLINES_SEPARATOR = False```

# Installation
Use the free [GitHubToFusion360](https://apps.autodesk.com/FUSION/en/Detail/Index?id=789800822168335025&os=Win64) add-in to install this script in Fusion 360.

Run the add-in and enter the URL of this repo: https://github.com/JeromeBriot/fusion360-import-spline-any-csv

# Usage

Run the ImportSplineAnyCSV script and select the CSV file containing the data to import.

![](/images/ImportSplineAnyCSV.png)

# Acknowledgement

This script is inspired by the "ImportSplineCSV" script from Autodesk. Some users faced issues when trying to import some CSV files using this script: [Import Spline CSV script "no valid points"](https://forums.autodesk.com/t5/fusion-360-support/import-spline-csv-script-quot-no-valid-points-quot/m-p/11702439). So I modified the part of the code where the data are read to make the reading more flexible.

# Support

Report issue, ask question or suggest new feature in this thread on the Autodesk Fusion 360 forum: [Import spline from any CSV file](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/script-importsplineanycsv/m-p/11708665)

Don't forget to attach the CSV file you try to import.

# Version history

- Version 1.3.0 - February 2025
  - Treat line in CSV file as empty if less than 3 characters

- Version 1.2.0 - February 2025
  - Add feature to import multiple splines from one CSV file
  - Add examples

- Version 1.1.0 - November 2024
  - Fix unique separator in CSV file reading.
  
- Version 1.0.0 - January 2023
  - First release.

# Licence
See the license.txt
