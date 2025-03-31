
#import statements
import os
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants_py as c

from motor_py import MOTOR
from sensor_py import SENSOR
from pyrosim.neuralNetwork import NEURAL_NETWORK  


#robot.py
class ROBOT:

  def __init__(self, body_file="body.urdf", brain_file="brain0.nndf", solutionID="0"):

    #Create dictionary for motors
    self.motors = {}
    #Load robot and prepare to simulate it
    self.robotId = p.loadURDF(body_file)

    #Shift the entire robot upward by 2 units so that it sits on top of runway.
    p.resetBasePositionAndOrientation(self.robotId, [0, 0, 2], [0, 0, 0, 1])
    #Prepare simulation using the robot's URDF ID
    pyrosim.Prepare_To_Simulate(self.robotId)

    # Create the neural network instance from brain.nndf
    self.nn = NEURAL_NETWORK(brain_file)  

    #Prepare to sense
    self.Prepare_To_Sense()

    #Prepare the motors
    self.Prepare_To_Act()

    os.system(f"rm {brain_file}")

  def Prepare_To_Sense(self):
    #Create sensors dictionary
    self.sensors = {}
    for linkName in pyrosim.linkNamesToIndices:
      self.sensors[linkName] = SENSOR(linkName)

  def Sense(self, t):
    # Iterate over all sensor instances and call their Get_Value method.
    for sensor in self.sensors.values():
        sensor.Get_Value(t)

  def Prepare_To_Act(self):
    # Create the motors dictionary.
    self.motors = {}
    # For each joint name in pyrosim.jointNamesToIndices, create a MOTOR instance.
    for jointName in pyrosim.jointNamesToIndices:
        self.motors[jointName] = MOTOR(jointName)

  def Act(self, t):
    # Iterate over all neuron names in the neural network.
    for neuronName in self.nn.Get_Neuron_Names():
        # Only process motor neurons.
        if self.nn.Is_Motor_Neuron(neuronName):
            jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
            desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJoinRange
            
            # Debug print statement.
            # Set the motor for the joint using the desired angle.
            pyrosim.Set_Motor_For_Joint(
                bodyIndex=self.robotId,
                jointName=jointName,
                controlMode=p.POSITION_CONTROL,
                targetPosition=desiredAngle,
                maxForce=100
            )
    
    
    #for motor in self.motors.values():
        #motor.Set_Value(self, t)
  
  def Think(self):
    #Update Sensor neuron values
    self.nn.Update()
    # Call the neural network's Print method.
    #self.nn.Print()
  

  def Get_Fitness(self):
    basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
    basePosition = basePositionAndOrientation[0]
    xPosition = basePosition[0]

    print("Fitness (x-coordinate):", xPosition)
    return xPosition