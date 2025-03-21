import sys
import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import constants_py as c

from simulation_py import SIMULATION
#simulate.py
if len(sys.argv) > 2:
    directOrGUI = sys.argv[1]  # "DIRECT" or "GUI"
    solutionID = sys.argv[2]   # e.g. "0" or "1"
else:
    # fallback if not provided
    directOrGUI = "DIRECT"
    solutionID = "0"
simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()