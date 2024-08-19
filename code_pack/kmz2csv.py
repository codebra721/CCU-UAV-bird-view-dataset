import pandas as pd
from pykml import parser
from zipfile import ZipFile
import os
import glob
import codecs
# # Step 1: Unzip KMZ file to get KML file
# with ZipFile('kml/2024-05-28 14-10-05.tlog.kmz', 'r') as zipObj:
#    # Extract all the contents of zip file in current directory
#    zipObj.extractall()

# Step 2: Parse the KML file
kml_filename = "kml/2024-05-28 14-10-05.tlog.kml"
with open(kml_filename, 'rb') as f:
    first_two_bytes = f.read(2)

# Check if the file starts with BOM
if first_two_bytes == codecs.BOM_UTF16:
    print('Detected UTF-16 encoding')
    encoding = 'utf-16'
else:
    print('Detected UTF-8 encoding')
    encoding = 'utf-8'

# Open the file with the detected encoding
with open(kml_filename, 'r', encoding=encoding) as f:
    kml_file = parser.parse(f)

# Step 3: Extract coordinates
coordinates = []
for placemark in kml_file.getroot().Folder.Placemark:
    coord = placemark.Model.Location
    lon= coord.longitude
    lat= coord.latitude
    alt= coord.altitude
    ori = placemark.Model.Orientation
    time = placemark.TimeStamp.when
    head = ori.heading 
    coordinates.append([float(lon), float(lat), float(head), float(alt), str(time)])

# Step 4: Create DataFrame and save as CSV
df = pd.DataFrame(coordinates, columns=['LON', 'LAT', 'HEA', 'altitude', 'time'])
df.to_csv('row_csv/gps_5.csv', index=False)

# # Remove the extracted KML file
# os.remove(kml_filename)