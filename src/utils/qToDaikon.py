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
# A .txt file as formatted by qscript.py, at the path specified below.
# 
# Output:
# ====================
# A properly formatted Daikon trace in the trace subdirectory of
# the current working directory, with the same timestamp as the  
# input qtrace-*.txt, now as a Daikon .dtrace file.
#
# ====================

import re

# Getting the input qtrace
txtIn = "trace/qtrace-20220804-121654.txt"
qt = open(txtIn, "rt")	# open the file in "read text" mode

# Find the timestamp of the input qtrace, and open a dtrace with that timestamp
# If your qtrace doesn't have a timestamp as formatted in qscript.py, 
tstamp = re.search(r"\d{8}-\d{6}",txtIn).group()
dt = open("trace/"+tstamp+".dtrace","wt")	# open in "write text" mode
					# NOTE: "wt" will OVERWRITE data if file exists

# Initialize empty lists for previous and current register values
oldVals = []
vals = []

nonce = 1	# the nonce monotonically increases at each program point (timepoint)

# loop through lines of qt
for l in qt:
	# find all register name/value pairs on current line
	# returns empty list if no register values found
	vals = re.findall(r"[a-z0-9/]+\s+[0-9a-f]{16}|\w+\s+[0-9a-f]x[0-9a-f]",l)

	# write timepoint to trace if nonempty and not equal to the previous cycle
	if vals != oldVals and vals:
		#print(vals)
		oldVals = vals
		# Holds all register/value lists at the current timepoint
		tpoint = []
		# entering program point
		dt.write("\n..tick():::ENTER\nthis_invocation_nonce\n"+str(nonce)+"\n")
		
		# Parse register/value pairs into lists
		for reg in vals:
			reg_val = re.split("\s+",reg)
			# hex string to int: `int("ff",16)` -> 255
			reg_val[1] = int(reg_val[1],16)
			# register name\n value \n constant 1
			dt.write(reg_val[0]+"\n"+str(reg_val[1])+"\n1\n")
			# for copying these values into the tick exit
			tpoint.append(reg_val)
		
		# exiting program point, passing in same values as entry
		dt.write("\n..tick():::EXIT0\nthis_invocation_nonce\n"+str(nonce)+"\n")
		for reg_val in tpoint:
			dt.write(reg_val[0]+"\n"+str(reg_val[1])+"\n1\n")
		
		nonce += 1	# finished with this timepoint, increment nonce for the next.

print("Trace converted!")

# close qtrace (all data has been read into internal structures)
qt.close()

# close dtrace (all values have been written to file)
dt.close()

