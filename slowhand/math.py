import math

def VecN(*args, n=3):
  if len(args) == n:
    return Vector(args)
  if len(args) == 1:
    try:
      len(args[0])
    except TypeError:
      return Vector(args * n) 
    if len(args[0]) == n:
      return Vector(args[0])
  raise TypeError

def Vec2(*args):
  return VecN(*args, n=2)

def Vec3(*args):
  return VecN(*args, n=3)

def Vec4(*args):
  return VecN(*args, n=4)

class Vector(object):
  def __init__(self, data):
    self.data = tuple(data)

  def __str__(self):
    return "({})".format(", ".join("{:.3f}".format(x) for x in self.data))

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

  def __neg__(self):
    return Vector(-x for x in self)
  
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

  def __rmul__(self, other):
    return self * other
  
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

class Ray(object):
  def __init__(self, origin, direction):
    self.origin = origin
    self.direction = direction.unit

  def __repr__(self):
    return "Ray<{}>".format(str(self))

  def __str__(self):
    return "{{Base: {}, Direction: {}}}".format(self.origin, self.direction)

  def trace(self, length):
    return self.origin + self.direction * length
  
  @property
  def inverse_direction(self):
    try:
      return self._inverse_direction
    except AttributeError:
      inf = float('inf')
      self._inverse_direction = Vector(1/x if x != 0 else inf
        for x in self.direction)
      return self._inverse_direction

  @property
  def sign(self):
    try:
      return self._sign
    except AttributeError:
      self._sign = Vector(int(x<0) for x in self.inverse_direction)
      return self._sign

AXIS_X = Vector((1, 0, 0))
AXIS_Y = Vector((0, 1, 0))
AXIS_Z = Vector((0, 0, 1))
