import sys
import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import constants_py as c

from simulation_py import SIMULATION
#simulate.py
if len(sys.argv) > 3:
    directOrGUI = sys.argv[1]  # e.g. "DIRECT"
    solutionID  = sys.argv[2]  # e.g. "1"
    videoFile   = sys.argv[3]  # e.g. "best_vid.mp4"
elif len(sys.argv) > 2:
    directOrGUI = sys.argv[1]
    solutionID  = sys.argv[2]
    videoFile   = "vid.mp4"
else:
    directOrGUI = "DIRECT"
    solutionID  = "0"
    videoFile   = "vid.mp4"


simulation = SIMULATION(directOrGUI, solutionID, videoFile)
simulation.Run()