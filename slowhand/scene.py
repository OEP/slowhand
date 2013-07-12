import math
from multiprocessing import cpu_count
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
      callback=None, box=None, threads=cpu_count()):
    self.camera = camera
    self.data = data
    self.scatter = scatter
    self.step = step
    self.samples = samples
    self.callback = callback
    self.box = box
    self.threads = threads

  def render(self, image):
    height, width, depth = image.shape
    for j in range(height):
      for i in range(width):
        light = self._do_render(i, j, width, height)
        if light:
          image[j][i] = light[:image.ndim]


  def _do_render(self, i, j, width, height):
    ray = self.camera.get_ray(i/width, j/height)
    t0 = self.camera.near
    t1 = self.camera.far
    light = Vec4(0)
    T = 1
    
    if self.callback:
      self.callback(j * width + i, width * height)

    if self.box:
      intersect = self.box.intersects(ray)
      if intersect:
        t0 = max(t0, intersect[0])
        t1 = min(t1, intersect[1])
      else:
        return None

    current = t0
    while T > 1e-6 and current < t1:
      x = ray.trace(current)
      deltaT = math.exp(-self.scatter * self.data.ed.eval(x) * self.step)
      light += self.data.ec.eval(x) * T * (1 - deltaT)
      T *= deltaT
      current += self.step
    
    return light
