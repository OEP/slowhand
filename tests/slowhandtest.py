import unittest
import math

class SlowhandTest(unittest.TestCase):
  DEFAULT_DELTA = 1e-6

  def assertVectorClose(self, actual, expected, d=DEFAULT_DELTA):
    if isinstance(d, (int, float)):
      d = (d,) * len(expected)
    for x,y,dd in zip(actual, expected, d):
      if not abs(x-y) < dd:
        raise AssertionError(
          "{} not in {} +/- {}".format(actual, expected, d))
  
  def assertClose(self, actual, expected, d=DEFAULT_DELTA):
    self.assertTrue(abs(actual-expected) < d,
      "{} not within {} +/- {}".format(actual, expected, d))
