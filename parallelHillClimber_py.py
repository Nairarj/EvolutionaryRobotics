import copy
from solution import SOLUTION
import constants_py as c

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        # Create a dictionary for storing parents
        self.parents = {}
        # Create populationSize random solutions
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION()

        # The instructions said to print the dictionary to verify:
        # print(self.parents)
        # Then remove the print statement, so we leave it commented out.

    def Evolve(self):
        # For now, we evaluate each parent in GUI mode, ignoring the generation loop.
        for i in self.parents:
            self.parents[i].Evaluate("GUI")
        # The rest of Evolve() code remains commented out or replaced with pass.
        # pass

    def Evolve_For_One_Generation(self, generation):
        # For now, just pass.
        pass

    def Show_Best(self):
        # For now, just pass.
        pass
