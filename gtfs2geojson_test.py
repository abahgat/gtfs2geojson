"""Tests for the GTFS2GeoJSON conversion script."""
import gtfs2geojson
import geojson
import os
import unittest

TEST_DATA_PATH = 'testdata'

class TestGtfs2Geojson(unittest.TestCase):
  def setUp(self):
    self.SAMPLE_COUNTS = {'AMV': 4, 'BEATTY_AIRPORT': 7, 'BULLFROG': 4,
        'DADAN': 2, 'EMSI': 2, 'FUR_CREEK_RES': 2, 'NADAV': 2, 'NANAA': 2,
        'STAGECOACH': 3}
    self.MINI_POINTS = {
        'S1': geojson.Feature(
            geometry={'type': 'Point', 'coordinates': ['-122.431282',
                                                       '37.728631']},
            properties={'count': 2, 'name': 'Mission St. & Silver Ave.'},
            id='S1'),
        'S2': geojson.Feature(
            geometry={'type': 'Point', 'coordinates': ['-122.422482',
                                                       '37.74103']},
            properties={'count': 1, 'name': 'Mission St. & Cortland Ave.'},
            id='S2')
    }

  def test_main_without_args_raises_error(self):
    with self.assertRaises(SystemExit):
      gtfs2geojson.main(['gtfs2geojson.py'])

  def test_parse_mini_feed(self):
    """Test that we parse correctly the static test data."""
    data = gtfs2geojson.read_from_directory(os.path.join(TEST_DATA_PATH,
                                                         'mini-feed'))
    self.assertIsNotNone(data)
    self.assertEqual(2, len(data.features))
    for feature in data.features:
      expected = self.MINI_POINTS[feature.id]
      self.assertEqual(expected.geometry.type, feature.geometry.type)
      self.assertEqual(expected.geometry.coordinates,
                       feature.geometry.coordinates)
      self.assertEqual(expected.properties, feature.properties)
      self.assertEqual(expected.id, feature.id)

  def test_parse_sample_feed_zip(self):
    """Test that we parse correctly the sample feed.

    Data from https://developers.google.com/transit/gtfs/examples/gtfs-feed"""
    data = gtfs2geojson.read_from_zip(os.path.join(TEST_DATA_PATH,
                                                   'sample-feed.zip'))
    self.assertIsNotNone(data)
    self.assertEqual(9, len(data.features))
    for feature in data.features:
      self.assertEqual('Point', feature.geometry.type)
      self.assertEqual(self.SAMPLE_COUNTS[feature.id],
                       feature.properties['count'])

  def test_convert_with_non_existing_file_fails(self):
    with self.assertRaises(gtfs2geojson.InputFileError):
      gtfs2geojson.convert('banana.txt')

  def test_convert_with_non_existing_zipfile_fails(self):
    with self.assertRaises(gtfs2geojson.InputFileError):
      gtfs2geojson.convert('banana.zip')

if __name__ == '__main__':
  unittest.main()