import numpy as np
import imageio
class Image(object):
  
  def __init__(self, width, height, depth=4):
    self.data = np.zeros((width, height, depth))
