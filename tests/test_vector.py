import math
from slowhandtest import SlowhandTest
from slowhand.math import Vector

class TestVector(SlowhandTest):
  def setUp(self):
    self.ones = Vector((1, 1, 1))
    self.zeros = Vector((0, 0, 0))
    self.tricky = Vector((1,2,3))

    self.x = Vector((1, 0, 0))
    self.y = Vector((0, 1, 0))
    self.z = Vector((0, 0, 1))

  def test_add(self):
    a = self.zeros + self.ones
    b = self.x + self.y + self.z
    self.assertEqual(a, self.ones)
    self.assertEqual(b, self.ones)

  def test_subtract(self):
    a = self.tricky - self.ones
    b = self.zeros - self.ones
    self.assertEqual(a, Vector((0,1,2)))
    self.assertEqual(b, Vector((-1, -1, -1)))

  def test_rotate(self):
    xx = self.y.rotate(self.z, math.pi / 2)
    yy = self.x.rotate(self.z, -math.pi / 2)
    zz = self.y.rotate(self.x, -math.pi / 2)

    self.assertVectorClose(xx, self.x)
    self.assertVectorClose(yy, self.y)
    self.assertVectorClose(zz, self.z)

  def test_dot(self):
    self.assertEqual(self.tricky * self.ones, 6)
    self.assertEqual(self.tricky * self.zeros, 0)

  def test_cross(self):
    xx = self.y ^ self.z
    yy = self.z ^ self.x
    zz = self.x ^ self.y

    self.assertEqual(xx, self.x)
    self.assertEqual(yy, self.y)
    self.assertEqual(zz, self.z)

  def test_unit(self):
    tricky = self.tricky
    ones = self.ones
    trickyMag = tricky.length
    onesMag = ones.length

    tricky = tricky.unit
    ones = ones.unit

    self.assertClose(tricky.length, 1.0)
    self.assertClose(ones.length, 1.0)
    self.assertVectorClose(tricky * trickyMag, self.tricky)
    self.assertVectorClose(ones * onesMag, self.ones)

