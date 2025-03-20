import os

from parallelHillClimber_py import PARALLEL_HILL_CLIMBER
#Run the simulatoon 5 times 
#os.system("python3 generate_py.py")
#os.system("python3 simulate_py.py")
phc = PARALLEL_HILL_CLIMBER()

#Calling Evolve method to evaluate the solution
phc.Evolve()
phc.Show_Best()

