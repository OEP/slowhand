import math

from slowhandtest import SlowhandTest
from slowhand.geom import Box
from slowhand.math import Vec3, AXIS_X, AXIS_Y, AXIS_Z, Ray

INTERSECTS = (
  Ray(Vec3(-2, 0, 0), AXIS_X),
  Ray(Vec3(0, -2, 0), AXIS_Y),
  Ray(Vec3(0, 0, -2), AXIS_Z),
  Ray(Vec3(2, 0, 0), -AXIS_X),
  Ray(Vec3(0, 2, 0), -AXIS_Y),
  Ray(Vec3(0, 0, 2), -AXIS_Z),
)
NOT_INTERSECTS = (
  Ray(Vec3(-3, 3, 0), AXIS_X),
  Ray(Vec3(0, -3, 3), AXIS_Y),
  Ray(Vec3(3, 0, -3), AXIS_Z),
  Ray(Vec3(2, 0, 3), -AXIS_X),
  Ray(Vec3(0, 2, 2), -AXIS_Y),
  Ray(Vec3(2, 0, 2), -AXIS_Z),
)
UNIT = Box.from_radius(1)

class TestBox(SlowhandTest):

  def test_intersects(self):
    for ray in INTERSECTS:
      self.assertEqual(UNIT.intersects(ray), (1, 3))
    for ray in NOT_INTERSECTS:
      self.assertEqual(UNIT.intersects(ray), None)
      
