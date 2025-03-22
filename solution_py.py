import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
import time

class SOLUTION:
  def __init__(self, myID):
    self.myID = myID
    self.weights = np.random.rand(3, 2)


    self.weights = self.weights * 2 - 1 
    self.fitness = 0.0
    


  def Start_Simulation(self, mode="DIRECT", video_filename="vid.mp4"):
        # Create the world, body, brain
        self.Create_Brain()
        # Build the command string:
        # e.g. python3 simulate_py.py DIRECT 0 &
        cmd = f"python3 simulate_py.py {mode} {self.myID} {video_filename} &"
        print("Starting simulation:", cmd)
        os.system(cmd)

  def Wait_For_Simulation_To_End(self):
        # 1) Poll for fitness{myID}.txt to appear
        fitnessFilename = f"fitness{self.myID}.txt"
        while not os.path.exists(fitnessFilename):
            time.sleep(0.01)

        # 2) Read it
        with open(fitnessFilename, "r") as f:
            fitness_str = f.read().strip()
        self.fitness = float(fitness_str)
        print(f"Solution {self.myID} fitness = {self.fitness}")

        # 3) Remove the fitness file
        os.system(f"rm {fitnessFilename}")



  def Create_World(self):
    pyrosim.Start_SDF("object.sdf")
    pyrosim.End()

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

  def Create_Brain(self):
    filename = f"brain{self.myID}.nndf"
    pyrosim.Start_NeuralNetwork(filename)
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
    randomRow = random.randint(0, 2)
    randomColumn = random.randint(0, 1)

    self.weights[randomRow][randomColumn] = random.random() * 2 - 1

  def Set_ID(self, newID):
    # If you need to assign a new ID to an existing solution (e.g. a child),
    # you can do so here
    self.myID = newID

