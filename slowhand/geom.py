
class Frustum(object):
  def __init__(self, apex, near, far, normal, up):
    self.apex = apex
    self.near = near
    self.far = far
    self.normal = normal / np.linalg.norm(normal)
    up = up / np.linalg.norm(up)
    right = np.cross(self.normal, up)
    up = np.

