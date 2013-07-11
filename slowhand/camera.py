import math
from .math import Ray, Vec3, AXIS_Z, AXIS_Y, AXIS_X
from .geom import Frustum

class Camera(object):
  def __init__(self,
      eye = Vec3(0),
      near = 0.001,
      far  = 100,
      hfov = math.radians(60),
      aspect_ratio = 1.7777777,
      view = AXIS_Z,
      up = AXIS_Y):
    self._frustum = Frustum(
      apex = eye,
      near = near,
      far = far,
      horizontal = hfov,
      vertical = hfov / aspect_ratio,
      normal = view,
      up = up)
    self._update()

  def look(self, *args):
    if len(args) == 3:
      eye = args[0]
      subject = args[1]
      up = args[2]
    elif len(args) == 9:
      eye = Vec3((args[0], args[1], args[2]))
      subject = Vec3((args[3], args[4], args[5]))
      up = Vec3((args[6], args[7], args[8]))
    else:
      raise TypeError
    self._frustum.apex = Vec3(eye)
    normal = subject - eye
    self._frustum.set_normal_up(normal, up)

  @property
  def near(self):
    return self._frustum.near

  @property
  def far(self):
    return self._frustum.far

  @property
  def eye(self):
    return self._frustum.apex

  @eye.setter
  def eye(self, value):
    self._frustum.apex = Vec3(value)

  @property
  def view(self):
    return self._frustum.normal

  @property
  def up(self):
    return self._frustum.up

  @property
  def right(self):
    return self._frustum.right

  @property
  def aspect_ratio(self):
    return self._frustum.horizontal / self._frustum.vertical

  @aspect_ratio.setter
  def aspect_ratio(self, value):
    self._frustum.vertical = self._frustum.horizontal / value
    self._update()

  @property
  def hfov(self):
    return self._frustum.horizontal

  @property
  def vfov(self):
    return self._frustum.vertical

  @hfov.setter
  def hfov(self, value):
    ar = self.aspect_ratio
    self._frustum.horizontal = value
    self.aspect_ratio = ar
    self._update()

  def get_ray_direction(self, x, y):
    x = (2 * x - 1.0) * self._tan_hfov
    y = (2 * y - 1.0) * self._tan_vfov
    return (y * self.up + x * self.right + self.view).unit

  def get_ray(self, x, y):
    direction = self.get_ray_direction(x, y)
    return Ray(self.eye + direction * self.near, direction)

  def _update(self):
    self._tan_hfov = math.tan(self.hfov / 2)
    self._tan_vfov = self._tan_hfov / self.aspect_ratio
