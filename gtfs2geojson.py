"""Converts GTFS data to GeoJSON.

The GTFS specification can be found here:
https://developers.google.com/transit/gtfs/reference"""

import csv
import geojson
import os
import sys
import tempfile
import zipfile

STOPS_FILE_NAME = 'stops.txt'
STOP_TIMES_FILE_NAME = 'stop_times.txt'

def read_from_zip(filename):
  """Read GTFS data from the specified zip file."""
  with zipfile.ZipFile(filename) as archive:
    temp_dir = tempfile.mkdtemp(suffix='gtfs2geojson')
    archive.extractall(temp_dir)
    return read_from_directory(temp_dir)

def read_from_directory(directory):
  """Read a GTFS directory and convert it to a GeoJSON feature collection."""
  # TODO(abahgat): raise error if directory does not exist
  with open(os.path.join(directory, STOPS_FILE_NAME), 'r') as stops_file:
    reader = csv.DictReader(stops_file)
    features = {}
    for row in reader:
      stop_id = row['stop_id']
      name = row['stop_name']
      latitude = float(row['stop_lat'])
      longitude = float(row['stop_lon'])
      feature = geojson.Feature(id=stop_id,
                                geometry=geojson.Point([longitude, latitude]),
                                properties={'count': 0,
                                            'name': name})
      features[stop_id] = feature
  with open(os.path.join(directory, STOP_TIMES_FILE_NAME), 'r') as times_file:
    reader = csv.DictReader(times_file)
    for row in reader:
      stop_id = row['stop_id']
      features[stop_id].properties['count'] += 1

  return geojson.FeatureCollection(features=features.values())

def convert(filename):
  if not os.path.exists(filename):
    raise InputFileError('The specified file was not found: %s' % filename)
  output = None
  if filename.endswith('.zip'):
    output = read_from_zip(filename)
  elif os.path.isdir(filename):
    output = read_from_directory(filename)
  else:
    raise InputFileError('Unrecognized input file, must be zip or directory')
  return stringify(output)

def stringify(item):
  return geojson.dumps(item)

def main(argv):
  if len(argv) < 2:
    sys.exit('Usage: %s GTFS_DIRECTORY.' % argv[0])
  print convert(argv[1])


class Error(Exception):
  pass

class InputFileError(Error):
  pass

if __name__ == '__main__':
  main(sys.argv)
