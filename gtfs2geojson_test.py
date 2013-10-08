"""Tests for the GTFS2GeoJSON conversion script."""
import gtfs2geojson
import os
import unittest

TEST_DATA_PATH = 'testdata'

class TestGtfs2Geojson(unittest.TestCase):
  def setUp(self):
    self.COUNTS = {'AMV': 4, 'BEATTY_AIRPORT': 7, 'BULLFROG': 4, 'DADAN': 2,
        'EMSI': 2, 'FUR_CREEK_RES': 2, 'NADAV': 2, 'NANAA': 2, 'STAGECOACH': 3}

  def test_main_without_args_raises_error(self):
    with self.assertRaises(SystemExit):
      gtfs2geojson.main(['gtfs2geojson.py'])

  def test_parse_sample_feed(self):
    """Test that we parse correctly the sample feed.

    Data from https://developers.google.com/transit/gtfs/examples/gtfs-feed"""
    data = gtfs2geojson.read(os.path.join(TEST_DATA_PATH, 'sample-feed'))
    self.assertIsNotNone(data)
    self.assertEqual(9, len(data.features))
    for feature in data.features:
      self.assertEqual('Point', feature.geometry.type)
      self.assertEqual(self.COUNTS[feature.id], feature.properties['count'])

if __name__ == '__main__':
  unittest.main()