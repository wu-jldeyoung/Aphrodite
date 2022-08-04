# Author: wu-jldeyoung on 2022-07-29
#
# Assumptions:
# ====================
# qemu-system-riscv64 is installed and configured correctly.
#
# A working copy of the riscv-gnu-toolchain is built on the
# system, with the environment variable $RISCV set to the
# toolchain build directory. The build I used was the
# riscv-unknown-linux-gnu- variant, configured with --enable-multilib.
#
# The toolchain install directory has been added to PATH.
# 
# Input:
# ====================
# A .txt file with register values as produced by QEMU's 
# monitor output from `info registers`, at the path specified below.
# 
# Output:
# ====================
# A properly formatted Daikon trace in the current working 
# directory, with the same timestamp as the input qtrace-*.txt, 
# now with the new dtrace- prefix.
#
# ====================

import re

# Getting the input qtrace
txtIn = "trace/qtrace-20220801-151842.txt"
qt = open(txtIn, "rt")	# open the file in "read text" mode

# Find the timestamp of the input qtrace, and open a dtrace with that timestamp
# If your qtrace doesn't have a timestamp as formatted in qscript.py, 
tstamp = re.search(r"\d{8}-\d{6}",txtIn).group()
dt = open(tstamp+".dtrace","wt")	# open in "write text" mode
					# NOTE: "wt" will OVERWRITE data if file already exists

# Initialize empty list to hold values at each timepoint
timepoints = []

oldVals = []
vals = []

# loop through lines of qt
for l in qt:
	# find all register name/value pairs on current line
	vals = re.findall(r"[a-z0-9/]+\s+[0-9a-f]{16}|\w+\s+[0-9a-f]x[0-9a-f]",l)

	# append to list of timepoints if nonempty
	if vals != oldVals and vals:
		#print(vals)
		timepoints.append(vals)
		oldVals = vals

print("We have "+str(len(timepoints))+" unique timepoints")

# Loop through list of timepoints and write to file
for i in range(len(timepoints)):
	print("\nAt timepoint "+str(i)+"\n====================")
	# Parse register/value pairs into "tuples"
	for j in range(len(timepoints[i])):
		reg_val = re.split("\s+",timepoints[i][j])
		reg = reg_val[0]
		val = int(reg_val[1],16)
		#print(reg_val)
		# hex string to int: `int("ff",16)` -> 255
		print("Register "+reg+"\thas value:\t"+str(val))


#close files
qt.close()
dt.close()

