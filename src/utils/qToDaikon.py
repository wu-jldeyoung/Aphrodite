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
# ====================

#import ???

txtIn = "file_to_parse.txt"

open(txtIn, "rt")
