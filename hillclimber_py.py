import copy
from solution_py import SOLUTION
from constants_py import numberOfGenerations

class HILL_CLIMBER:
  def __init__(self):
    #Creating a random solution as the parent
    self.parent = SOLUTION()

  
  def Evolve(self):
    self.parent.Evaluate("initial_vid.mp4")

    for currentGeneration in range(numberOfGenerations):
      self.Evolve_For_One_Generation(currentGeneration)
    
    self.Show_Best()
  
  def Evolve_For_One_Generation(self, generation):
    self.Spawn()
    self.Mutate()
    self.child.Evaluate("child_vid.mp4")

    self.PrintFitness(generation)

    self.Select()

  
  def PrintFitness(self, generation):
    print(f"Generation {generation}: "
          f"Parent fitness: {self.parent.fitness}, "
          f"Child fitness: {self.child.fitness}")
  
  def Spawn(self):
    self.child = copy.deepcopy(self.parent)

  def Mutate(self):
    self.child.Mutate()

  def Select(self):
    if self.parent.fitness > self.child.fitness:
        self.parent = self.child

  
  def Show_Best(self):
    self.parent.Evaluate("final_vid.mp4")
