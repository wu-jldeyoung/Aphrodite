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
tstamp = re.search(r"\d{8}-\d{6}",txtIn).group()
dt = open(tstamp+".dtrace","wt")	# open in "write text" mode
					# NOTE: "wt" will OVERWRITE data if file already exists

# Initialize empty list to hold values at each timepoint
timepoints = []

# loop through lines of qt
for l in qt:
	# find all register name/value pairs on current line
	vals = re.findall(r"\w+\s+[0-9a-f]{16}|\w+\s+[0-9a-f]x[0-9a-f]",l)
	#print(i)
	i += 1
	# append to list of timepoints if nonempty
	if vals:
		#print(vals)
		timepoints.append(vals)

print("We have "+str(len(timepoints))+" timepoints")


#close files
qt.close()
dt.close()

