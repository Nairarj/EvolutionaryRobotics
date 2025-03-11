import random
import matplotlib.pyplot as plt
import numpy as np
import pybullet as p
import pybullet_data
import imageio_ffmpeg
import pyrosim.pyrosim as pyrosim
import time
import constants_py as c
from base64 import b64encode
from IPython.display import HTML
from tempfile import TemporaryFile
from world_py import WORLD
from robot_py import ROBOT

#simulation.py
class SIMULATION:

  def __init__(self):

    # physics parameters.
    self.physicsClient = p.connect(p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8, self.physicsClient)

    #creation of world and robot objects
    self.world = WORLD()
    self.robot = ROBOT()

  def Run(self):

    # camera parameters
    cam_target_pos = [0, 0, 1.5]
    cam_distance = 12.5
    cam_yaw, cam_pitch, cam_roll = -50, -20, 0
    cam_width, cam_height = 480, 368
    cam_up, cam_up_axis_idx, cam_near_plane, cam_far_plane, cam_fov = [0, 0, 1], 2, 0.01, 100, 60



    # Initialize video.
    vid = imageio_ffmpeg.write_frames('vid.mp4', (cam_width, cam_height), fps=30)
    vid.send(None) # The first frame of the video must be a null frame.

    for t in range(c.iterations):
      #current_target = targetAngles[t]

      #backLegMotorValues[t] = current_target
      #frontLegMotorValues[t] = current_target

      #pyrosim.Set_Motor_For_Joint(bodyIndex = self.robotId, jointName = b"Torso_BackLeg", controlMode = p.POSITION_CONTROL, targetPosition = backLegMotorAngles[t], maxForce = 100)
      #pyrosim.Set_Motor_For_Joint(bodyIndex = self.robotId, jointName = b"Torso_FrontLeg", controlMode = p.POSITION_CONTROL, targetPosition= frontLegMotorAngles[t], maxForce = 100)


      # Create one image and add it to the video.
      cam_view_matrix = p.computeViewMatrixFromYawPitchRoll(cam_target_pos, cam_distance, cam_yaw, cam_pitch, cam_roll, cam_up_axis_idx)
      cam_projection_matrix = p.computeProjectionMatrixFOV(cam_fov, cam_width*1./cam_height, cam_near_plane, cam_far_plane)
      image = p.getCameraImage(cam_width, cam_height,cam_view_matrix, cam_projection_matrix)[2][:, :, :3]
      vid.send(np.ascontiguousarray(image))
      cam_yaw = cam_yaw + 1

      # Do physics stuff.
      #print("Loop index:", t)
      p.stepSimulation()
      self.robot.Sense(t)
      #Adding call to Think()
      self.robot.Think()
      self.robot.Act(t)
      time.sleep(1/300)

    vid.close()

def __del__(self):
    try:
        p.disconnect()
    except Exception:
        pass