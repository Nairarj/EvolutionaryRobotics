import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
import time

class SOLUTION:
  def __init__(self, index=0):
    self.weights = np.random.rand(3, 2)


    self.weights = self.weights * 2 - 1

    self.index = index 
    self.fitness = 0.0


  def Evaluate(self, video_filename="vid.mp4"):
    # Create unique filenames for URDF, SDF, NNDF, and fitness
    self.world_file  = f"world_{self.index}.sdf"
    self.body_file   = f"body_{self.index}.urdf"
    self.brain_file  = f"brain_{self.index}.nndf"
    self.fitness_file= f"fitness_{self.index}.txt"
    #Generate the robot world, body, and brain using solution weights
    self.Create_World()
    self.Create_Body()
    self.Create_Brain()
    # Set environment variables so simulate.py knows which files to load.
    os.environ["WORLD_FILE"]   = self.world_file
    os.environ["BODY_FILE"]    = self.body_file
    os.environ["BRAIN_FILE"]   = self.brain_file
    os.environ["FITNESS_FILE"] = self.fitness_file

    os.environ["VIDEO_FILENAME"] = video_filename
    os.system("python simulate.py &")

    def Wait_For_Fitness(self):
      # Wait until the fitness file is created.
      while not os.path.exists(self.fitness_file):
          time.sleep(0.01)

      # Now read it.
      with open(self.fitness_file, "r") as f:
          fitness_str = f.read().strip()
      self.fitness = float(fitness_str)
  


  def Create_World(self):
    pyrosim.Start_SDF("object.sdf")
    pyrosim.End()
    # Optional: wait until file is physically written out
    while not os.path.exists(self.world_file):
        time.sleep(0.01)

  def Create_Body(self):
    #Fixed dimensions
    width = 1.0
    length = 1.0
    height = 1.0
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[width, length, height])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1.0, 0, 1.0])
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[width, length, height])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2.0, 0, 1.0])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[width, length, height])
    pyrosim.End()

    # Optional wait
    while not os.path.exists(self.body_file):
        time.sleep(0.01)

  def Create_Brain(self):
    pyrosim.Start_NeuralNetwork("brain.nndf")
    # Create sensor neurons (names 0,1,2 with link names)
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
    # Create motor neurons (names 3,4 with joint names)
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
    # Fully connected synapses: iterate over sensor neurons (rows) and motor neurons (columns)
    for currentRow in range(3):   # 0, 1, 2 for sensor neurons
        for currentColumn in range(2):   # 0, 1 for motor neurons (target name = currentColumn + 3)
            weight = self.weights[currentRow][currentColumn]
            pyrosim.Send_Synapse(sourceNeuronName=currentRow, 
                                  targetNeuronName=currentColumn + 3, 
                                  weight=weight)
    pyrosim.End()

  def Mutate(self):
    ranndomRow = random.randint(0, 2)
    randomColumn = random.randint(0, 1)

    self.weights[ranndomRow][randomColumn] = random.random() * 2 - 1
