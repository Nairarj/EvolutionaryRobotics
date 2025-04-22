import numpy as np

#constants.py
iterations = 200
backAmplitude = np.pi / 8
backFrequency = 5
backPhaseOffset = 0


frontAmplitude = np.pi / 4
frontFrequency = 5
frontPhaseOffset = np.pi/2

motorJoinRange = 0.2
numberOfGenerations = 3
populationSize = 3

numSensorNeurons = 4
numMotorNeurons = 8

#M4 : A/B testing flags
#Switch between the two fitness functions: "A" or "B"
FITNESS_MODE = "B"
#Only record one video (the best at the end)
RENDER_VIDEO = False
RUNWAY_HALF_WIDTH = 1.5