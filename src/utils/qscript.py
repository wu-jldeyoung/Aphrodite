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
# A linked ELF file compiled and linked for riscv64, 
# at location specified by the variable path below.
# 
# Output:
# ====================
# A .txt file, with register values as formatted by QEMU's
# internal logging tools and the monitor command `info registers`.
#
# ====================

import datetime as dt
#import subprocess as sp
#import threading
import shlex
#import signal
import time
#import os
import pexpect as px

# For now, we'll go with ~/Desktop/riscv-hello-world/asm/hello
# Config file? Leave hard-coded?

# location of a linked ELF file compiled for riscv64
path = "/home/jldey/Desktop/riscv-hello-world/asm/hello"

# get current time for file-naming
curT = dt.datetime.now()
tSim = curT.strftime("%Y%m%d-%H%M%S")

# commandline arguments for QEMU, tokenized according to shlex.split()
args = ["qemu-system-riscv64", 
	"-machine",
	#"sifive_e", 
	"virt", 	# see QEMU documentation for more details, or use qemu-system-riscv64 -machine help
	"-kernel", path, 	# launches the file at path on the guest system
	"-monitor", "stdio", 	# sends QEMU monitor to stdio (specified below in the subprocess call)
	"-S",			# starts the guest paused
	"-d", "cpu",		# logs cpu state (register values) to file specified by -D
	"-D",			# creates log file with the below name in the current working directory
	"./logs/qpyLog"+tSim+".txt"
	]

# create a Python file object for writing traces
# opening in 'x' mode will return an error if the file already exists
# "qtrace" prefix specifies that this is a QEMU-formatted trace (not Daikon)

trace = open("trace/qtrace-"+tSim+".txt", "xt")
trace.write("QEMU trace "+curT.strftime("%Y-%m-%d %H:%M:%S")+"\n\n=====================\n\n")


# run QEMU with args as arguments, shell-escaped for security
qemu = px.spawn(shlex.join(args))
print("child process created")

# grab initial state
qemu.expect(".*\r\n(qemu)")
qemu.sendline("info registers")

# tell QEMU to continue execution ("c")
qemu.expect("(qemu)")
qemu.sendline("c")
print("continuing")

# pipe "info registers" to QEMU
# TODO: parse QEMU output to Daikon format
# TODO: while not timed out
for i in range(10):
	trace.write(str(qemu.before) + "\n\n=====================\n\n")
	print(str(i+1)+" reg vals written")
	qemu.expect("(qemu)")
	qemu.sendline("info registers")

# quit QEMU and close the subprocess
qemu.expect("(qemu)")
qemu.sendline("q")
trace.write(str(qemu.before) + "\n\n=====================\n\n")

print("quit QEMU")

trace.close()
