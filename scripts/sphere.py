from slowhand.scene import Scene, RenderData
from slowhand.camera import Camera
from slowhand.math import Vec3, Vec4
from slowhand.geom import Box
import numpy as np
import imageio

class UnitSphere(object):
  def eval(self, x):
    return max(0, min(1, 1 - x.length))

class White(object):
  def eval(self, x):
    return Vec4(1)

class Callback(object):
  def __init__(self):
    self.last = None
    self.count = 0

  def update(self, current, total):
    self.count += 1
    pct = int(100 * self.count / total)
    if self.last is None:
      self.last = pct-1
    if pct > self.last:
      print(pct, self.count, total)
      self.last = pct

def main():
  c = Camera(near=2, far=4)
  c.look(0, 0, 4, 0, 0, 0, 0, 1, 0)
  data = RenderData(
    ed = UnitSphere(),
    ec = White())
  scene = Scene(c, data)
  width = 200
  height = width / c.aspect_ratio
  depth = 3
  image = np.zeros((width, height, depth), dtype=np.float32)
  cb = Callback()
  scene.callback = cb.update
  scene.box = Box.from_radius(1)
  scene.render(image)
  imageio.imsave('sphere.exr', image)

if __name__ == "__main__":
  main()
