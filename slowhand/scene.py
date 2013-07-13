import math
from multiprocessing import cpu_count, Pool
from collections import namedtuple
from .math import Vec3, Vec4

def patch_generator(patchx, patchy, width, height):
  for px in range(0, width, patchx):
    for py in range(0, height, patchy):
      yield px, py, px + patchx, py + patchy

class RenderData(object):
  def __init__(self, ed=None, ec=None, sd=None, sc=None, sm=[]):
    self.ed = ed
    self.ec = ec
    self.sd = sd
    self.sc = sc
    self.sm = sm

class Scene(object):
  def __init__(self, camera, data, scatter=5, step=0.1, samples=1,
      callback=None, box=None, threads=cpu_count(), patch_size=100):
    self.camera = camera
    self.data = data
    self.scatter = scatter
    self.step = step
    self.samples = samples
    self.callback = callback
    self.box = box
    self.threads = threads
    self.patch_size = patch_size

  def render(self, image):
    height, width, depth = image.shape
    def yield_args(x1, y1, x2, y2):
      for j in range(y1, y2):
        for i in range(x1, x2):
          if 0 <= i < width and 0 <= j < height:
            yield i, j, width, height

    patchinfo = self.patch_size, self.patch_size, width, height
    pool = Pool(self.threads)
    for x1, y1, x2, y2 in patch_generator(*patchinfo):
      result = pool.map(self._do_render, yield_args(x1, y1, x2, y2))

      for i, j, light in result:
        if light:
          image[j][i] = light[:image.ndim]
      
  def _do_render(self, args):
    i, j, width, height = args
    ray = self.camera.get_ray(i/width, j/height)
    t0 = self.camera.near
    t1 = self.camera.far
    light = Vec4(0)
    T = 1

    if self.box:
      intersect = self.box.intersects(ray)
      if intersect:
        t0 = max(t0, intersect[0])
        t1 = min(t1, intersect[1])
      else:
        return i, j, None

    current = t0
    while T > 1e-6 and current < t1:
      x = ray.trace(current)
      deltaT = math.exp(-self.scatter * self.data.ed.eval(x) * self.step)
      light += self.data.ec.eval(x) * T * (1 - deltaT)
      T *= deltaT
      current += self.step
    
    return i, j, light
