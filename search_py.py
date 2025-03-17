import os

from hillclimber_py import HILL_CLIMBER
#Run the simulatoon 5 times 
#os.system("python3 generate_py.py")
#os.system("python3 simulate_py.py")
hc = HILL_CLIMBER()

#Calling Evolve method to evaluate the solution
hc.Evolve()

