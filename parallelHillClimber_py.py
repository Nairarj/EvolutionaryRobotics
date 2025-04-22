import copy
import numpy as np 
from solution_py import SOLUTION
import constants_py as c
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        # Clean up any leftover brain or fitness files from previous runs
        os.system("rm brain*.nndf 2> /dev/null")     # On Mac/Linux
        os.system("rm fitness*.txt 2> /dev/null")    # On Mac/Linux

        #Variable to track the next available unique ID
        self.nextAvailableID = 0
        # Create a dictionary for storing parents
        self.parents = {}
        # Create populationSize random solutions
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

        #M4 - allocate one matrix to record fitness per [individual, generation]
        self.fitnessMatrix = np.zeros((c.populationSize, c.numberOfGenerations))
        # The instructions said to print the dictionary to verify:
        #print(self.parents)
        # Then remove the print statement, so we leave it commented out.

    def Evolve(self):
        # 1) Evaluate all parents in parallel
        self.Evaluate(self.parents)
        # TEMP: exit right after evaluating parents for debugging
        # print("Exiting after evaluating parents.")
        # exit()

        # 2) Loop over generations
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(currentGeneration)
 
        self.Show_Best()

        #M4 - save the fitness matrix for later plotting
        filename = "fitnessA.npy" if c.FITNESS_MODE == "A" else "fitnessB.npy"
        np.save(filename, self.fitnessMatrix)
        print(f"\n saved fitness matrix to {filename}\n")

    def Evolve_For_One_Generation(self, generation):
        self.Spawn()

        self.Mutate()

        self.Evaluate(self.children)
        #M4 - record each child's fitness in the matrix
        for i, child in self.children.items():
          self.fitnessMatrix[i, generation] = child.fitness

        self.Print(generation)

        self.Select()


    def Spawn(self):
        self.children = {}
        # For each parent, create a child
        for i in self.parents:
            # deep copy the ith parent
            child = copy.deepcopy(self.parents[i])
            # assign a new ID
            child.myID = self.nextAvailableID
            self.nextAvailableID += 1
            # store it in self.children
            self.children[i] = child

  
    def Mutate(self):
        # Mutate each child in self.children
        for i in self.children:
            self.children[i].Mutate()


    def Evaluate(self, solutions):
        """
        Evaluate the given dictionary of solutions in parallel:
         1) Start each simulation in parallel
         2) Wait for each simulation to end
        """
        # Start simulations in parallel
        for i in solutions:
            solutions[i].Start_Simulation("DIRECT")

        # Then wait for them to finish and get fitness
        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()




    def Select(self):
      for i in self.parents:
        if self.children[i].fitness < self.parents[i].fitness:
            # child is better, so adopt the parent's old ID
            oldID = self.parents[i].myID
            self.children[i].myID = oldID  # keep the parent's ID
            print(f"Replacing parent {i} (ID={oldID}) with child {i} (ID was {self.children[i].myID}).")
            self.parents[i] = self.children[i]



    def Print(self, generation):
        print("\n--- Parent vs Child Fitness ---")
        for i in self.parents:
            print(f"Gen {i}: Parent Fit = {self.parents[i].fitness}, "
                  f"Child Fit = {self.children[i].fitness}")
        print("\n")


    def Show_Best(self):
      """ Re-simulate the best parent in DIRECT mode, producing best_vid.mp4. """
      # Find the parent with the lowest fitness
      bestKey = min(self.parents, key=lambda i: self.parents[i].fitness)
      bestFitness = self.parents[bestKey].fitness
      print(f"\nBest solution is key {bestKey}, with fitness {bestFitness}")

      # Re-run this solution in DIRECT mode, producing a new video file
      

      #M4 - enable video only for this one run
      import constants_py as c 
      c.RENDER_VIDEO = True
      # We'll treat it like "GUI" but in Colab it's still just a video
      self.parents[bestKey].Start_Simulation("DIRECT", "best_vid.mp4")
      # We do not call Wait_For_Simulation_To_End() because we already have its fitness
      # If you want to re-read the fitness, you could do so, but it's not required.
      print("Simulating the best solution in DIRECT mode. Video: best_vid.mp4\n")

