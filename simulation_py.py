import sys
import random
import matplotlib.pyplot as plt
import numpy as np
import pybullet as p
import pybullet_data
import imageio_ffmpeg
import pyrosim.pyrosim as pyrosim
import time
import constants_py as c
import os
from base64 import b64encode
from IPython.display import HTML
from tempfile import TemporaryFile
from world_py import WORLD
from robot_py import ROBOT

#simulation.py
class SIMULATION:

  def __init__(self, directOrGUI="DIRECT", solutionID="0", video_filename="vid.mp4"):
    self.directOrGUI = directOrGUI
    self.solutionID = solutionID
    self.video_filename= video_filename

    if directOrGUI == "GUI":
    # In real local PyBullet, we might do p.connect(p.GUI)
    # But in Colab, just do p.connect(p.DIRECT).
      self.physicsClient = p.connect(p.DIRECT)
    else:
      self.physicsClient = p.connect(p.DIRECT)
    
    
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8, self.physicsClient)

    #creation of world and robot objects
    self.world = WORLD("object.sdf")
    brainFile = f"brain{solutionID}.nndf"
    self.robot = ROBOT("body.urdf", brainFile, solutionID)

  def Run(self):
    # camera parameters
    cam_target_pos = [0, 0, 1.5]
    cam_distance = 12.5
    cam_yaw, cam_pitch, cam_roll = -50, -20, 0
    cam_width, cam_height = 480, 368
    cam_up, cam_up_axis_idx, cam_near_plane, cam_far_plane, cam_fov = [0, 0, 1], 2, 0.01, 100, 60



    # Initialize video.

    vid = imageio_ffmpeg.write_frames(self.video_filename, (cam_width, cam_height), fps=30)
    vid.send(None) # The first frame of the video must be a null frame.

    timeOnRunway = 0
    for t in range(c.iterations):
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
      baseY = p.getBasePositionAndOrientation(self.robot.robotId)[0][1]
      if abs(baseY) <= c.RUNWAY_HALF_WIDTH:
        timeOnRunway += 1
      #time.sleep(1/300)

    vid.close()

    self.Get_Fitness(timeOnRunway)

  def Get_Fitness(self, timeOnRunway):
    # 1) Read base position
    xPos, yPos = p.getBasePositionAndOrientation(self.robot.robotId)[0][:2]
    forward  = max(0.0, xPos)
    avgSpeed = forward / c.iterations

    if c.FITNESS_MODE == "B":
        # If the robot ever fell off (didn't stay all timesteps), zero reward
      if timeOnRunway < c.iterations:
          rawFitness = 0.0
          print(f"Fell off at t={timeOnRunway}/{c.iterations}; rawFitness=0")
      else:
          # Perfect run: reward pure average speed
          rawFitness = avgSpeed
          print(f"Raw Fitness B: perfect run, avgSpeed = {avgSpeed:.4f}")
    else:
        if abs(yPos) >= c.RUNWAY_HALF_WIDTH:
            lateralPenalty = 0.0
        else:
            lateralPenalty = 1 - (abs(yPos)/c.RUNWAY_HALF_WIDTH)**2
        rawFitness = avgSpeed * lateralPenalty
        print(f"Fitness A: avgSpeed {avgSpeed:.4f} * lateralPenalty {lateralPenalty:.2f} = {rawFitness:.4f}")

    # 2) Negate for minimizer
    fitness_value = -rawFitness

    # 3) Write out
    tmpFile = f"tmp{self.solutionID}.txt"
    with open(tmpFile, "w") as f:
        f.write(str(fitness_value))
    os.system(f"mv {tmpFile} fitness{self.solutionID}.txt")
        
def __del__(self):
    try:
        p.disconnect()
    except Exception:
        pass

if __name__=="__main__":
    # Expect 2 arguments: mode and solutionID
    if len(sys.argv) > 2:
        directOrGUI = sys.argv[1]   # e.g. "DIRECT" or "GUI"
        solutionID = sys.argv[2]    # e.g. "0" or "1"
    else:
        directOrGUI = "DIRECT"
        solutionID = "0"

    sim = SIMULATION(directOrGUI, solutionID)
    sim.Run()