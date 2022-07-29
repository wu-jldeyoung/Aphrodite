# Author: jldeyoung on 2022-07-??

# Assumptions:
# qemu-system-riscv64 is installed and configured correctly.
# A working copy of the riscv-gnu-toolchain is built on the system,
# with the environment variable $RISCV set to the toolchain build
# directory. The build I used was the riscv-unknown-linux-gnu-,
# configured with --enable-multilib.
# The toolchain install directory has been added to PATH.

import os
import datetime as dt
import subprocess as sp
import shlex

# For now, we'll go with ~/Desktop/riscv-hello-world/asm/hello
# Config file? Leave hard-coded?

# location of a linked ELF file compiled for riscv64
# if Qemu gives "" error, check input file
path = "/home/jldey/Desktop/riscv-hello-world/asm/hello"

# commandline arguments for QEMU, tokenized according to shlex.split()
args = ["qemu-system-riscv64", 
		"-machine", "virt", 	# see QEMU documentation for more details, or use qemu-system-riscv64 -machine help
		"-kernel", path, 		# launches the file at path on the guest system
		"-monitor", "stdio", 	# sends QEMU monitor to stdio (specified below in the subprocess call)
		"-S",					# starts the guest paused
		"-d", "cpu",			# logs cpu state (register values) to file specified by -D
		"-D", "./qpyLog"+dt.datetime.now().strftime("%Y%m%d-%H%M%S")+".txt"]
								# creates log file with this name in the current working directory

# copy current environment variables into a dict for use by subprocess
env = os.environ.copy()

# run QEMU with args as arguments
# shell = True has the potential for shell injection, as noted in documentation
# However, it may be that using shlex.join(), as done here, can mitigate this injection vulnerability.
# shlex.join() is shell-escaped
# env=env may be unnecessary here, but keeping it in seems like good practice for portability

# stdin, stdout, and stderr can be directed to an existing file object.
# subprocess.run() waits for a process to complete. Popen() may be more useful to us here.

#s = sp.run(shlex.join(args), stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT, text=True, env = env)

# need a Popen object to communicate with child process
# PIPE is a file object (stream?) that handles I/O to and from the child process.

# The following results in undefined behavior when called on the list args
# but executes as expected when called on args joined into a single string.
s = sp.run(shlex.join(args), shell=True, text=True, env=env)
print("Past call to sp.run()")

s = sp.Popen(shlex.join(args), shell=True, text=True, env=env)
print("Past call to sp.Popen()")

# At approximately 18:04, I used Ctrl+D EOF to try to ensure the script had stopped execution, and lost my terminal :(

# THREE EQUIVALENT EXPRESSIONS:
#==============================
#os.system(" ".join(args))
#retcode = sp.call(" ".join(args), shell=True)
#s = sp.run(" ".join(args), shell=True, text=True)
#==============================

# pipe "info registers\n" to QEMU


# tell the monitor to continue execution ("c\n")

# loop time! Do a couple that send "info registers\n"

#quit QEMU

