import math

class Vector(object):
  def __init__(self, data):
    self.data = tuple(data)

  def __str__(self):
    return str(self.data)

  def __repr__(self):
    return "Vector<{}>".format(str(self))
  
  def __len__(self):
    return len(self.data)

  def __getitem__(self, i):
    return self.data[i]

  def __eq__(self, other):
    if isinstance(other, Vector):
      if len(other) != len(self):
        raise TypeError("Mismatched dimensions.")
      return all([x==y for x,y in zip(self, other)])
    return NotImplemented
  
  def __xor__(self, other):
    if isinstance(other, Vector):
      return self.cross(other)
    return NotImplemented

  def __mul__(self, other):
    if isinstance(other, Vector):
      return self.dot(other)
    if isinstance(other, (int, float)):
      return Vector(x*other for x in self)
    return NotImplemented
  
  def __add__(self, other):
    if isinstance(other, Vector):
      if len(other) != len(self):
        raise TypeError("Mismatched dimensions.")
      return Vector(x+y for x,y in zip(self, other))
    return NotImplemented

  def __sub__(self, other):
    if isinstance(other, Vector):
      if len(other) != len(self):
        raise TypeError("Mismatched dimensions.")
      return Vector(x-y for x,y in zip(self, other))
    return NotImplemented

  def __truediv__(self, other):
    if isinstance(other, Vector):
      if len(other) != len(self):
        raise TypeError("Mismatched dimensions.")
      return Vector(x/y for x,y in zip(self, other))
    if isinstance(other, (int, float)):
      return Vector(x/other for x in self)
    return NotImplemented

  @property
  def length(self):
    try:
      return self._length
    except AttributeError:
      self._length = math.sqrt(sum([x*x for x in self.data]))
      return self._length

  @property
  def unit(self):
    try:
      return self._unit
    except AttributeError:
      self._unit = self / self.length
      return self._unit

  def dot(self, other):
    if len(other) != len(self):
      raise TypeError("Mismatched dimensions.")
    return sum(x*y for x,y in zip(self, other))

  def cross(self, other):
    if len(self) != 3 or len(other) != 3:
      raise TypeError("Not a 3D Vector.")
    return Vector((
      self[1] * other[2] - self[2] * other[1],
      self[2] * other[0] - self[0] * other[2],
      self[0] * other[1] - self[1] * other[0],
    ))
  
  def rotate(self, axis, theta):
    if len(self) != 3 or len(axis) != 3:
      raise TypeError("Not a 3D Vector.")
    axis = axis.unit
    return (
      self * math.cos(theta) +
      axis * (self * axis) * (1 - math.cos(theta)) +
      (self ^ axis) * math.sin(theta))
