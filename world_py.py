import pybullet as p
import pybullet_data
import numpy
import pyrosim.pyrosim as pyrosim

#world.py
class WORLD:

  def __init__(self):

    self.plane_id = p.loadURDF("plane.urdf")
    p.loadSDF("object.sdf")
