# Author: wu-jldeyoung on 2022-07-??
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
# ====================

import os
import datetime as dt
import subprocess as sp
import shlex

# For now, we'll go with ~/Desktop/riscv-hello-world/asm/hello
# Config file? Leave hard-coded?

# location of a linked ELF file compiled for riscv64
path = "/home/jldey/Desktop/riscv-hello-world/asm/hello"

# commandline arguments for QEMU, tokenized according to shlex.split()
args = ["qemu-system-riscv64", 
	"-machine", "virt", 	# see QEMU documentation for more details, or use qemu-system-riscv64 -machine help
	"-kernel", path, 	# launches the file at path on the guest system
	"-monitor", "stdio", 	# sends QEMU monitor to stdio (specified below in the subprocess call)
	"-S",			# starts the guest paused
	"-d", "cpu",		# logs cpu state (register values) to file specified by -D
	"-D",			# creates log file with the below name in the current working directory
	"./logs/qpyLog"+dt.datetime.now().strftime("%Y%m%d-%H%M%S")+".txt"
	]

# create a Python file object for writing traces
# opening in 'x' mode will return an error if the file already exists
# "qtrace" prefix specifies that this is a QEMU-formatted trace (not Daikon)
trace = open("trace/qtrace-"+dt.datetime.now().strftime("%Y%m%d-%H%M%S")+".txt", "xt")

# copy current environment variables into a dict for use by subprocess
env = os.environ.copy()

# run QEMU with args as arguments
# shell = True has the potential for shell injection, as noted in documentation.
# However, it may be that using shlex.join(), as done here, can mitigate this 
# injection vulnerability, as shlex.join() is shell-escaped.
# env=env may be unnecessary here, but keeping it in seems like good practice 
# for portability

#s = sp.run(shlex.join(args), stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT, text=True, env = env)

qemu = sp.Popen(shlex.join(args), shell=True, text=True, env=env)
print("Past call to sp.Popen()")

# pipe "info registers\n" to QEMU

# tell the monitor to continue execution ("c\n")

# loop time! Do a couple that send "info registers\n"

# quit QEMU and close the subprocess

