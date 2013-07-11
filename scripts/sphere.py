from slowhand.scene import Scene, RenderData
from slowhand.camera import Camera
from slowhand.math import Vec3, Vec4
import numpy as np
import imageio

class UnitSphere(object):
  def eval(self, x):
    return min(0, max(1, 1 - x.length))

class White(object):
  def eval(self, x):
    return Vec4(1)

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
  image = imageio.imread('/home/pkilgo/Desktop/pyfx-sphere.png')
  print(image.shape)
  scene.render(image)
  imageio.imsave('sphere.png', image)

if __name__ == "__main__":
  main()
