import math
from collections import namedtuple
from .math import Vec3, Vec4

class RenderData(object):
  def __init__(self, ed=None, ec=None, sd=None, sc=None, sm=[]):
    self.ed = ed
    self.ec = ec
    self.sd = sd
    self.sc = sc
    self.sm = sm

class Scene(object):
  def __init__(self, camera, data, scatter=5, step=0.1, samples=1,
      callback=None):
    self.camera = camera
    self.data = data
    self.scatter = scatter
    self.step = step
    self.samples = samples
    self.callback = callback

  def render(self, image):
    width, height, depth = image.shape
   
    for j in range(height):
      for i in range(width):
        ray = self.camera.get_ray(i/width, j/height)
        t0 = self.camera.near
        t1 = self.camera.far
        current = t0
        T = 1
        light = Vec4(0)

        while T > 1e-6 and current < t1:
          x = ray.trace(current)
          deltaT = math.exp(-self.scatter * self.data.ed.eval(x) * self.step)
          light += self.data.ec.eval(x) * T * (1 - deltaT)
          T *= deltaT
          current += self.step
        
        image[i][j] = light[:image.ndim]
        if self.callback:
          self.callback(j * width + i, width * height)
