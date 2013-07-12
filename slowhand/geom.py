import math
import sys
from .math import Vector, Vec3, AXIS_X, AXIS_Y

class Frustum(object):
  def __init__(self, apex, near, far, horizontal, vertical, normal, up):
    self.apex = apex
    self.near = near
    self.far = far
    self.horizontal = horizontal
    self.vertical = vertical
    self.normal = None
    self.up = None
    self.right = None
    self.set_normal_up(normal, up)

  def set_normal_up(self, normal, up):
    self.normal = normal.unit
    up = up.unit
    self.right = self.normal.cross(up)
    self.up = up.cross(self.right)

class Box(object):
  def __init__(self, llc, urc):
    self.bounds = [llc, urc]

  @classmethod
  def from_radius(cls, r):
    r = abs(r)
    return cls(Vec3(-r), Vec3(r))

  def intersects(self, r):
    tmin = (self.bounds[r.sign[0]][0] - r.origin[0]) * r.inverse_direction[0]
    tmax = (self.bounds[1-r.sign[0]][0] - r.origin[0]) * r.inverse_direction[0]

    tymin = (self.bounds[r.sign[1]][1] - r.origin[1]) * r.inverse_direction[1]
    tymax = (self.bounds[1-r.sign[1]][1] - r.origin[1]) * r.inverse_direction[1]

    if(tmin > tymax or tymin > tmax):
      return None

    tmin = max(tmin, tymin)
    tmax = min(tmax, tymax)

    tzmin = (self.bounds[r.sign[2]][2] - r.origin[2]) * r.inverse_direction[2]
    tzmax = (self.bounds[1-r.sign[2]][2] - r.origin[2]) * r.inverse_direction[2]

    if(tmin > tzmax or tzmin > tmax):
      return None

    tmin = max(tmin, tzmin)
    tmax = min(tmax, tzmax)

    t0 = max(tmin,  0.0)
    t1 = min(tmax, sys.float_info.max)

    if(t1 < t0):
      t0, t1 = t1, t2

    return (t0, t1)
