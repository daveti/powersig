#!/usr/bin/python

# PowerSig Data Visualizer
# CPU/CPU or CPU/MEM data visualization
# Usuage: ./visualizer data.csv
# Apr 15, 2015
# root@davejingtian.org
# http://davejingtian.org

import sys
import numpy as np
import matplotlib.pyplot as plt

# Make sure there are 2 arguments
if len(sys.argv) != 2:
	print("Error: invalid number of arguments")
	sys.exit()

# Read the data
with open(sys.argv[1]) as f:
	data = f.read()

data = data.split('\n')
data = filter(None, data)

x = [row.split(',')[0] for row in data]
y = [row.split(',')[1] for row in data]

# Convert to float
x_f = []
for e in x:
	x_f.append(float(e))

y_f = []
for e in y:
	y_f.append(float(e))

# Plot it
plt.title("Power Signature")
plt.plot(x_f, y_f, 'ro')
plt.axis([0, 10, 0, 10])
plt.grid(True)
plt.show()
