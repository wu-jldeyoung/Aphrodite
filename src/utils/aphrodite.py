# Author: wu-jldeyoung on 2022-08-05
#
# Input:
# ====================
# A linked ELF file compiled and linked for riscv64, 
# at location specified by the variable path below,
# and a timeout (specified in minutes)
# 
# Output:
# ====================
# A Daikon .dtrace file named with a timestamp. Use the 
# included universal.decls (or run make_decls.py) before
# invoking Daikon on the generated trace.
#
# ====================

import pexpect as px
import datetime
import shlex
import time
import re
import os

# location of a linked ELF file compiled for riscv64
path = "/home/jldey/Downloads/riscv-fedora-images/" # directory where elf file is located
exe = path+"Fedora-Minimal-Rawhide-20200108.n.0-fw_payload-uboot-qemu-virt-smode.elf" # name of elf file
drv = path+"Fedora-Minimal-Rawhide-20200108.n.0-sda.raw" # for booting Linux, gives "drive" option for QEMU

#path = "/home/jldey/Desktop/riscv-hello-world/asm/"
#exe = path+"hello"

# timeout in minutes
timeout = 120

# get current time for file-naming
init = datetime.datetime.now()
tSim = init.strftime("%Y%m%d-%H%M%S")

# generate datetime of timeout
end = datetime.datetime(init.year, init.month, init.day, init.hour+int(timeout/60), (init.minute+timeout)%60, init.second)

# commandline arguments for QEMU, tokenized according to shlex.split()
args = ["-machine", 
	"virt", 	# see QEMU documentation for more details, or use qemu-system-riscv64 -machine help
	"-kernel", exe, 	# launches the file at path on the guest system
	"-monitor", "stdio", 	# sends QEMU monitor to stdio (specified below in the subprocess call)
	"-S",			# starts the guest paused
	
	# options for running Fedora
	"-smp","4",
	"-m","2G",
	"-bios", "none",
   	"-object", "rng-random,filename=/dev/urandom,id=rng0",
   	"-device", "virtio-rng-device,rng=rng0",
   	"-device", "virtio-blk-device,drive=hd0",
   	"-drive", "file="+drv+",format=raw,id=hd0",
   	"-device", "virtio-net-device,netdev=usernet",
   	"-netdev", "user,id=usernet,hostfwd=tcp::10000-:22"
	]
	# These options from deprecated version of qscript.py. 
	# They are not necessary, and are included for
	#"-d", "cpu",		# logs cpu state (register values) to file specified by -D
	#"-D",			# creates log file with the below name in the current working directory
	#"./logs/qpyLog"+tSim+".txt"

#os.system("qemu-system-riscv64 "+" ".join(args))
	

# Initialize empty lists for previous and current register values
oldVals = []
vals = []

nonce = 1	# the nonce monotonically increases at each program point (timepoint)

# create a Python file object for writing the trace
# opening in 'x' mode will return an error if the file already exists
dt = open("trace/"+tSim+".dtrace", "xt")


# run QEMU with args as arguments
qemu = px.spawn("qemu-system-riscv64", args, encoding="utf-8")
print("child process created")

# grab initial state
qemu.expect(".*(qemu)")
qemu.sendline("info registers")

# tell QEMU to continue execution ("c")
qemu.expect("(qemu)")
qemu.sendline("c")
print("continuing")


# while not timed out
while datetime.datetime.now() < end:
	
	#print("In while loop")
	
	# grab `info registers` output
	out = qemu.before
	#print(out)
	
	# find all register name/value pairs on current line
	# returns empty list if no register values found,
	# i.e. the output was not a string of register/value pairs
	vals = re.findall(r"[a-z0-9/]+\s+[0-9a-f]{16}|\w+\s+[0-9a-f]x[0-9a-f]",out)
	
	# write timepoint to trace if nonempty and not equal to the previous cycle
	if vals != oldVals and vals:
		#print(vals)
		oldVals = vals
		# Holds all register/value lists at the current timepoint
		tpoint = []
		# entering program point
		dt.write("\n..tick():::ENTER\nthis_invocation_nonce\n"+str(nonce)+"\n")
		print("Entering program point: "+str(nonce))
		
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
		print("Exiting program point: "+str(nonce))
		for reg_val in tpoint:
			dt.write(reg_val[0]+"\n"+str(reg_val[1])+"\n1\n")
		
		print("Finished program point: "+str(nonce))
		nonce += 1	# finished with this timepoint, increment nonce for the next.

	# send the next `info registers` command
	qemu.expect("(qemu)")
	qemu.sendline("info registers")

# quit QEMU, close the subprocess, and close the trace.
qemu.expect("(qemu)")
qemu.sendline("q")

print("quit QEMU")

dt.close()
