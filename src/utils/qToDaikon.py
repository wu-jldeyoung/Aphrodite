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
# built-in logging function or the monitor output from 
# `info registers`, at the path specified below.
# 
# Output:
# ====================
# A properly formatted Daikon trace in the current working 
# directory, with the same timestamp as the input qtrace-*.txt, 
# now with the new dtrace- prefix.
#
# IDEAL FUNCTIONALITY:
# ====================
# - this tool is "qtrace-agnostic" (either a log trace or a 
#   monitor trace)
#	- support for monitor traces will be prioritized, as
#	  they contain FPRs.
#
# ====================

import re

# Getting the input qtrace
txtIn = "file_to_parse.txt"
open(txtIn, "rt")	# open the file in "read text" mode


# the regular expression at the heart of this script
re.findall(r"\w+\s+[0-9a-f]{16}|\w+\s+[0-9a-f]x[0-9a-f]",txt)










