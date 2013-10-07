"""Tests for the GTFS2GeoJSON conversion script."""
import gtfs2geojson
import unittest

class TestGtfs2Geojson(unittest.TestCase):
  def test_main_without_args_raises_error(self):
    with self.assertRaises(SystemExit):
      gtfs2geojson.main(['gtfs2geojson.py'])

if __name__ == '__main__':
  unittest.main()