import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
import time
import constants_py as c

class SOLUTION:
  def __init__(self, myID):
    self.myID = myID
    self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)


    self.weights = self.weights * 2 - 1 
    self.fitness = 0.0
    


  def Start_Simulation(self, mode="DIRECT", video_filename="vid.mp4"):
        # Create the world, body, brain
        self.Create_World()
        self.Create_Body()
        
        self.Create_Brain()
        # Build the command string:
        # e.g. python3 simulate_py.py DIRECT 0 &
        cmd = f"python3 simulate_py.py {mode} {self.myID} {video_filename} 2>&1 &"
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
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 2], size=[width, length, height])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0.0, -0.5, 2.0], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="BackLeg", pos=[0.0, -0.5, 0.0], size=[0.2, 1.0, 0.2])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0.0, 0.5, 2.0], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.0, 0.5, 0.0], size=[0.2, 1.0, 0.2])
    pyrosim.Send_Joint(name="Torso_LeftLeg",parent="Torso",child="LeftLeg",type="revolute",position=[-0.5, 0.0, 2.0],jointAxis="0 1 0")
    pyrosim.Send_Cube(name="LeftLeg",pos=[-0.5, 0.0, 0.0],size=[1.0,0.2,0.2])
    pyrosim.Send_Joint(name="Torso_RightLeg",parent="Torso",child="RightLeg",type="revolute",position=[0.5, 0.0, 2.0],jointAxis="0 1 0")
    pyrosim.Send_Cube(name="RightLeg",pos=[0.5, 0.0, 0.0],size=[1.0,0.2,0.2])

    # 1) FRONT LOWER LEG
    pyrosim.Send_Joint(
        name="FrontLeg_FrontLowerLeg",
        parent="FrontLeg",
        child="FrontLowerLeg",
        type="revolute",
        position=[0.0, 1.0, 0.0],   # at the bottom of the front leg
        jointAxis="1 0 0"
    )
    pyrosim.Send_Cube(
        name="FrontLowerLeg",
        pos=[0.0, 0.5, 0.0],       # halfway down that link
        size=[0.2, 1.0, 0.2]
    )

    # 2) BACK LOWER LEG
    pyrosim.Send_Joint(
        name="BackLeg_BackLowerLeg",
        parent="BackLeg",
        child="BackLowerLeg",
        type="revolute",
        position=[0.0, -1.0, 0.0], # bottom of the back leg
        jointAxis="1 0 0"
    )
    pyrosim.Send_Cube(
        name="BackLowerLeg",
        pos=[0.0, -0.5, 0.0],
        size=[0.2, 1.0, 0.2]
    )

    # 3) LEFT LOWER LEG
    pyrosim.Send_Joint(
        name="LeftLeg_LeftLowerLeg",
        parent="LeftLeg",
        child="LeftLowerLeg",
        type="revolute",
        position=[-1.0, 0.0, 0.0], # bottom of the left leg
        jointAxis="1 0 0"
    )
    pyrosim.Send_Cube(
        name="LeftLowerLeg",
        pos=[-0.5, 0.0, 0.0],
        size=[1.0, 0.2, 0.2]
    )

    # 4) RIGHT LOWER LEG
    pyrosim.Send_Joint(
        name="RightLeg_RightLowerLeg",
        parent="RightLeg",
        child="RightLowerLeg",
        type="revolute",
        position=[1.0, 0.0, 0.0],  # bottom of the right leg
        jointAxis="1 0 0"
    )
    pyrosim.Send_Cube(
        name="RightLowerLeg",
        pos=[0.5, 0.0, 0.0],
        size=[1.0, 0.2, 0.2]
    )

    pyrosim.End()

  def Create_Brain(self):
    filename = f"brain{self.myID}.nndf"
    pyrosim.Start_NeuralNetwork(filename)
    # Create sensor neurons (names 0,1,2,3,4 with link names)
    #pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    #pyrosim.Send_Sensor_Neuron(name=1, linkName="FrontLeg")
    pyrosim.Send_Sensor_Neuron(name=0, linkName="FrontLowerLeg")
    #pyrosim.Send_Sensor_Neuron(name=3, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLowerLeg")
    #pyrosim.Send_Sensor_Neuron(name=5, linkName="LeftLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="LeftLowerLeg")
    #pyrosim.Send_Sensor_Neuron(name=7, linkName="RightLeg")
    pyrosim.Send_Sensor_Neuron(name=3, linkName="RightLowerLeg")
    # Create motor neurons (names 5,6,7,8 with joint names)
    pyrosim.Send_Motor_Neuron(name=9,  jointName="Torso_FrontLeg")
    pyrosim.Send_Motor_Neuron(name=10, jointName="FrontLeg_FrontLowerLeg")
    pyrosim.Send_Motor_Neuron(name=11, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=12, jointName="BackLeg_BackLowerLeg")
    pyrosim.Send_Motor_Neuron(name=13, jointName="Torso_LeftLeg")
    pyrosim.Send_Motor_Neuron(name=14, jointName="LeftLeg_LeftLowerLeg")
    pyrosim.Send_Motor_Neuron(name=15, jointName="Torso_RightLeg")
    pyrosim.Send_Motor_Neuron(name=16, jointName="RightLeg_RightLowerLeg")

    # Fully connected synapses: iterate over sensor neurons (rows) and motor neurons (columns)
    for currentRow in range(c.numSensorNeurons):   # 0, 1, 2 for sensor neurons
        for currentColumn in range(c.numMotorNeurons):   # 0, 1 for motor neurons (target name = currentColumn + 3)
            weight = self.weights[currentRow][currentColumn]
            motorName = 9 + currentColumn
            pyrosim.Send_Synapse(sourceNeuronName=currentRow, 
                                  targetNeuronName=motorName, 
                                  weight=weight)
    pyrosim.End()
    
    #exit()

  def Mutate(self):
    randomRow = random.randint(0, c.numSensorNeurons - 1)
    randomColumn = random.randint(0, c.numMotorNeurons - 1)

    self.weights[randomRow][randomColumn] = random.random() * 2 - 1

  def Set_ID(self, newID):
    # If you need to assign a new ID to an existing solution (e.g. a child),
    # you can do so here
    self.myID = newID

