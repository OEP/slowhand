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

  def update(self, current, total):
    pct = int(100 * current / total)
    if self.last is None:
      self.last = pct-1
    if pct > self.last:
      print(pct, current, total)
      self.last = pct

def main():
  c = Camera(near=2, far=4)
  c.look(0, 0, 4, 0, 0, 0, 0, 1, 0)
  data = RenderData(
    ed = UnitSphere(),
    ec = White())
  scene = Scene(c, data)
  width = 720
  height = width / c.aspect_ratio
  depth = 3
  #image = np.zeros((width, height, depth))
  image = imageio.imread('/home/pkilgo/Desktop/better-bunny.png')
  cb = Callback()
  scene.callback = cb.update
  scene.box = Box.from_radius(1)
  print(image.shape)
  scene.render(image)
  imageio.imsave('sphere.png', image)

if __name__ == "__main__":
  main()
