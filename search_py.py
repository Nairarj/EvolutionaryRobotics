import os

#Run the simulatoon 5 times 
for i in range(5):
  print("Simulation iteration:", i+1)
  os.system("python3 generate_py.py")
  os.system("python3 simulate_py.py")
