import math
from .math import Vector, AXIS_X, AXIS_Y
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
