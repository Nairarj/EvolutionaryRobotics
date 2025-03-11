import pybullet as p
import pybullet_data
import numpy as np
import pyrosim.pyrosim as pyrosim

import constants_py as c

#sensor.py
class SENSOR:

  def __init__(self, linkName):

      # Save the link name in the instance.
      self.linkName = linkName
      # Create a sensor vector (filled with zeros).
      self.values = np.zeros(c.iterations)

  def Get_Value(self, t):
    if self.linkName == b"Torso":
        self.values[t] = 1.0  # <-- Force torso sensor value to 1.0
    else:
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

  def Save_Values(self):
      # Save the sensor values vector to a file.
      np.save("sensor_" + self.linkName + ".npy", self.values)
     