#### 2022-05-25

Starting from Ubuntu 20.04

Following https://github.com/pulp-platform/pulp-runtime/blob/master/README.md

	$ sudo apt install git python3-pip gawk texinfo libgmp-dev libmpfr-dev libmpc-dev
	$ sudo pip3 install pyelftools

Cloning repositories into jldey@ubuntu:~/Repos/pulp
	
	$ git clone --recursive https://github.com/pulp-platform/pulp-riscv-gnu-toolchain

so now we should have the toolchain installed, if all's well. Now, toolchain 
dependencies:

	$ sudo apt-get install autoconf automake autotools-dev curl libmpc-dev libmpfr-dev 
	  libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc 
	  zlib1g-dev

### 2022-06-10

https://youtu.be/27tndT6cBH0
https://pulp-platform.org/docs/riscv_workshop_zurich/schiavone_wosh2019_tutorial.pdf

- energy-efficient, open-source programmable microcontroller
	- use in IoT devices
	- "Parallel Ultra Low Power"
- PULPissimo architecture
	- RISC-V based microcontroller with peripherals
		
### 2022-06-16

# meeting notes:

Adding PATH variables

- export PATH=$PATH:/opt/riscv/bin
- echo PATH before and after changes
- save PATH before changing it (in case of bricked systems)
	- export OLDPATH=$PATH
	- echo $PATH >oldpath.txt

- get *either* 32-bit or 64-bit working with *some* extensions
	- focus on 32-bit, no extensions rv32i

- Look at Qemu -- emulation environment (runs test suite)
	
# work progress

adding to PATH
	
- old path: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
	
	$ export PATH=$PATH:/opt/riscv/bin
	
	PATH modified successfully.
	
	$ ./configure --prefix=/opt/riscv
		- this is telling me that there is no such file or directory as 
		  'configure'---did I add the wrong thing to PATH?
			-> try changing the PATH addition to the directory of the 
			   installation
	$ make linux

### 2022-06-21

The problem wasn't my PATH. What I needed to do was:

	$ cd Repos/pulp/pulp-riscv-gnu-toolchain

This allowed me to run the configure command that was in the repository that we 
cloned earlier. Hopefully, if this completes successfully, I will have 
configured the toolchain.

It did not complete successfully. I ~~may~~ have run out of disk space.

New vm created, with 100GB disk space. Here's hoping.

[If this still doesn't work, try appending /opt/riscv/bin to the *beginning* 
of PATH, not the end.]

IT WORKED!!!
The successful one was the Newlib version, which uses the commands:
	
	$ ./configure --prefix=/opt/riscv
	$ make

### 2022-06-22

Installing and configuring Qemu: https://wiki.qemu.org/Hosts/Linux

	$ sudo apt-get install git libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev ninja-build
	
	$ sudo apt-get install git-email
	$ sudo apt-get install libaio-dev libbluetooth-dev libcapstone-dev libbrlapi-dev libbz2-dev
	$ sudo apt-get install libcap-ng-dev libcurl4-gnutls-dev libgtk-3-dev
	$ sudo apt-get install libibverbs-dev libjpeg8-dev libncurses5-dev libnuma-dev
	$ sudo apt-get install librbd-dev librdmacm-dev
	$ sudo apt-get install libsasl2-dev libsdl2-dev libseccomp-dev libsnappy-dev libssh-dev
	$ sudo apt-get install libvde-dev libvdeplug-dev libvte-2.91-dev libxen-dev liblzo2-dev
	$ sudo apt-get install valgrind xfslibs-dev
	
	$ git clone git://git.qemu-project.org/qemu.git
	
	$ # Switch to the QEMU root directory.
	$ cd qemu
	$ # Prepare a native debug build.
	$ mkdir -p bin/debug/native
	$ cd bin/debug/native
	$ # Configure QEMU and start the build.
	$ ../../../configure --enable-debug
	$ make
	$ # Return to the QEMU root directory.
	$ cd ../../..
	
	$ bin/debug/native/x86_64-softmmu/qemu-system-x86_64 -L pc-bios

I have the test BIOS working. Now, to see what we can do with qemu and the PULP 
toolchain.

	$ ./configure --prefix=$RISCV --disable-linux --with-arch=rv64ima # or --with-arch=rv32ima
	$ make newlib 
	$ make check-gcc-newlib
	
	$ ./configure --prefix=$RISCV
	$ make linux 
	
This step is resulting in errors. I might need to add the following qemu stuff 
to PATH, although I'm not sure what directory I'll find it in.
	
	$ # Need qemu-riscv32 or qemu-riscv64 in your `PATH`.
	$ make check-gcc-linux

### 2022-07-08

parallel process: generate traces from *anything* on qemu

look into verilator

PROCESS OVERVIEW (high-level):

1. Get RISC-V/PULPissimo running in emulation or simulation
2. Use simulation tools to generate logs/outputs of as much information about 
	register transfers as possible
3. Parse those logs and outputs into a trace

IMMEDIATE GOAL: emulate the RISC-V ISA and run Linux.
	
### 2022-07-11
	
# Simulation vs. Emulation

- simulation runs like a whole processor, with wires and all
- emulation recreates an ISA

1. Verify qemu works with a bare-metal C program
2. Try running Linux on the virt RISC-V

https://jasonblog.github.io/note/arm_emulation/hello_world_for_bare_metal_arm_using_qemu.html
I took this test program as an example of C written for bare metal.

Task 1. was proving too much to wrap my head around today, so I went back to 
https://wiki.qemu.org/Documentation/Platforms/RISCV#Booting_64-bit_Fedora
to try and boot Fedora. Lo and behold, I got it to work, with one minor 
alteration (*RULE #1, never trust the README*):

	login: root
	password: fedora_rocks!

Let's try some basic things here:

	$ ls
	$ mkdir jldey
	$ cd jldey
	
all seemed to work as expected.

	$ echo "Hello World!"
	$ echo $PATH > path.txt
	$ cat path.txt

also worked as expected.

Shutdown:

	$ /sbin/shutdown -h

See [the session transcript](/fedora-session-2022-07-11.txt) for more details.


### 2022-07-12

getting register values through DEBUG ports
	
- a Qemu setting (debug? trace?)

Try new risc-v C compilers

- research error 306 on the PULP riscv-gcc

Inspired by our meeting this morning, I did some background reading on RISC,
MIPS, and ARM.

# Why would Intel choose not to use a RISC approach?

CISC architecture allows for "higher programming productivity" in Assembly. It 
also means fewer instructions will be used to compile high-level programs.

**fewer instructions --> less heat produced per time**
*This is an electrical engineering result, which is not apparent from our level 
of research (ISA level).*

Microcoding allows emulation of wider word length---
**allowing greater compatibility between different products in a family**
---but so does the RISC-V standard

RISC is better from a CS standpoint, CISC is better for the e. engineers
and the physicists.

Bash tutorial: figuring out if there's a new file
	
	$ ls -al > before.txt
	$ ./compile
	$ ls -al > after.txt
	$ diff before.txt after.txt > diff.txt
	$ cat diff.txt
	

### 2022-07-13

Memory sinkhole--differences between CISC and RISC designs

# Configuring the new toolchain

Since the PULP toolchain is for PULP architecture and not the Qemu `virt` 
machine, I grabbed the riscv-gnu-toolchain instead:

	$ git clone https://github.com/riscv/riscv-gnu-toolchain --recursive

*Despite* what the README would have you believe, the `--recursive` *is* 
necessary to clone the submodules.

Next, as recommended, I installed dependencies.

	$ sudo apt-get install autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev

I got the riscv-gnu-toolchain built successfully using the following commands:
	
	$ ./configure --prefix=/opt/riscv --enable-multilib
	$ sudo make

To verify that it built and configured correctly, I tried compiling my `hello.c`
from my example bare metal C for ARM. That attempt produced the following 
result:

	jldey@ubuntu:~/Repos/riscv-gnu-toolchain/riscv-gcc$ chmod 777 compile -v
	jldey@ubuntu:~/Repos/riscv-gnu-toolchain/riscv-gcc$ ./compile ~/Desktop/hello.c
	/home/jldey/Desktop/hello.c: 1: Syntax error: "(" unexpected

I have *never* in my life been so happy to encounter a compile error. Now, we 
work on finding out what the hell went wrong.

### 2022-07-13

Test program: change the value of a register and detect that it was changed:

- less complex: integer addition
- more complex: "Hello World!"

**use an assembly program to generate a trace**

1. ANYTHING running on Qemu (asm or C)
2. Get register values out of Qemu

This [RISC-V bare-metal assembly "Hello World!"](https://theintobooks.wordpress.com/2019/12/28/hello-world-on-risc-v-with-qemu/#comments)
referenced the [riscv-probe](https://github.com/michaeljclark/riscv-probe), 
which is a "simple machine mode program to probe RISC-V control and status 
registers." I believe this will be important for generating traces. But first, I 
had to install its dependencies, starting with [riscv-tools](https://github.com/riscv/riscv-tools),
which keeps failing to build on my system.
	
	$ sudo apt-get install autoconf automake autotools-dev curl libmpc-dev libmpfr-dev libgmp-dev libusb-1.0-0-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev device-tree-compiler pkg-config libexpat-dev
	$ git clone https://github.com/riscv-software-src/riscv-tools.git
	$ cd riscv-tools
	$ git submodule update --init --recursive
	$ export RISCV=/home/jldey/Repos/riscv-toolchain/ # install directory for the toolchain
	$ ./build.sh

The build fails at the `Configuring project riscv-pk` step, with the following 
error codes:
	
	Configuring project riscv-pk
	Building project riscv-pk
	gcc: error: unrecognized argument in option ‘-mcmodel=medany’
	gcc: note: valid arguments to ‘-mcmodel=’ are: 32 kernel large medium small
	make: *** [Makefile:319: file.o] Error 1

I'm not sure what that means, so we'll just move on for the time being.
[Revisited on 2022-07-18](#2022-07-18)

# Running the [assembly Hello World](https://theintobooks.wordpress.com/2019/12/28/hello-world-on-risc-v-with-qemu/#comments)

After copying the included assembly into a file called `hello.s`, I created the 
makefile and [linker script](https://github.com/michaeljclark/riscv-probe/blob/master/env/qemu-sifive_u/default.lds) 
`link.lds` as specified.

It turns out that I had ***not,*** in fact, configured my toolchain correctly. I
again tried the `./configure` and `make` steps for the `riscv-gnu-toolchain`, 
still with `/opt/riscv/bin` as my install directory.

I had to try this several times, getting unhelpful `Error 1` and `Error 2` 
messages in the `make` process. On the advice of the README, I cleared out my 
install directory before trying to install again into the same directory. I 
tried the following, and this seemed to work:
	
	$ ./configure --prefix=/opt/riscv --enable-multilib
	$ sudo make linux

The process teminated, and I verified that there were executable files in 
`/opt/riscv/bin`.

### 2022-07-15

I finally figured out how to invoke my newly configured `riscv-gcc`, with the 
following command:

	$ riscv64-unknown-linux-gnu-gcc --help

This produced a help menu. I next tried to compile `hello.c`, and recieved this 
error message:

	$ riscv64-unknown-linux-gnu-gcc ~/Desktop/hello.c
	
	riscv64-unknown-linux-gnu-gcc: error trying to exec 'cc1': execvp: No such file or directory

I then invoked verbose mode with the `-v` flag and tried compiling again, with 
this output:

	Using built-in specs.
	COLLECT_GCC=riscv64-unknown-linux-gnu-gcc
	Target: riscv64-unknown-linux-gnu
	Configured with: /home/jldey/Repos/pulp/pulp-riscv-gnu-toolchain/riscv-gcc/configure --target=riscv64-unknown-linux-gnu --prefix= --with-sysroot=/sysroot --with-newlib --without-headers --disable-shared --disable-threads --with-system-zlib --enable-tls --enable-languages=c --disable-libatomic --disable-libmudflap --disable-libssp --disable-libquadmath --disable-libgomp --disable-nls --disable-bootstrap --enable-checking=yes --disable-multilib --with-abi=lp64d --with-arch=rv64imafdc
	Thread model: single
	gcc version 7.1.1 20170509 (GCC) 
	COLLECT_GCC_OPTIONS='-v' '-march=rv64imafdc' '-mabi=lp64d'
	 cc1 -quiet -v -iprefix /usr/bin/../lib/gcc/riscv64-unknown-linux-gnu/7.1.1/ /home/jldey/Desktop/hello.c -quiet -dumpbase hello.c -march=rv64imafdc -mabi=lp64d -auxbase hello -version -o /tmp/ccuBhus5.s
	riscv64-unknown-linux-gnu-gcc: error trying to exec 'cc1': execvp: No such file or directory

From this output, it seems that my `./configure --enable-multilib` flag had not,
for whatever reason, configured multilib support. I did find it somewhat odd 
that there were no `riscv32-...` executables in `/opt/riscv/bin`, which was the 
first sign that it didn't configure multilib. Since the `riscv-probe` requires a
multilib installation, I'll have to try again (but I'll use a different install 
directory, because I *have* a working `riscv-gcc` right now, even if it's only 
for the 64-bit architecture. --> It seems that I didn't read far enough on the 
toolchain README, and the Linux multilib cross-compiler uses the prefix 
`riscv64-unknown-linux-gnu-`, although it can target *both* 32-bit and 64-bit 
systems. Since I knew my 64-bit `virt` emulator was working, I opted to use that
for my target.

Let's try to build our Assembly hello world, instead of C. Since I've tested the 
`virt` machine in Qemu, I'll try targeting it with my assembler and linker. To 
do this, I looked up the `UART0` address for `virt`, which I found on line 85 of 
`qemu/hw/riscv/virt.c`:

	static const MemMapEntry virt_memmap[] = {
	...
		[VIRT_UART0] =	{	0x10000000,	0x100	},
	...
	};

In accordance with this, I changed line 5 of `hello.s` to be 

	lui t0, 0x10000

since that is the line that loads our UART0 address into register t0. As noted 
in [my annotations of this assembly](/src/Assembly_Hello/riscv-hello-asm_annotated), 
`lui` loads the given 20-bit immediate into the upper 20 bits of the destination 
register `rd`, in this case, `t0`.

**EXIT QEMU: 'Ctrl+A' then 'x'**

To run the program, I had to change the [Makefile](/src/Assembly_Hello/Makefile) 
so that it would invoke my Linux glibc multilib cross-compiler rather than the 
Newlib 32-bit cross-compiler used in the example:

	hello: hello.o link.lds
		riscv64-unknown-linux-gnu-ld -T link.lds -o hello hello.o

	hello.o: hello.s
		riscv64-unknown-linux-gnu-as -o hello.o hello.s

	clean:
		rm hello hello.o

This Makefile takes `hello.s` as input, then runs it through the assembler, 
which produced the ELF file `hello.o`, and finally ran `hello.o` through the 
linker, to produce the linked ELF file `hello`. Now, we are ready to run our 
program in Qemu, which I did with the following:

	$ cd ~/Repos/Qemu
	$ qemu-system-riscv64 -machine virt -nographic -kernel ~/Desktop/hello

This produced the following output:

	qemu-system-riscv64: warning: No -bios option specified. Not loading a firmware.
	qemu-system-riscv64: warning: This default will change in a future QEMU release. Please use the -bios option to avoid breakages when this happens.
	qemu-system-riscv64: warning: See QEMU's deprecation documentation for details.
	Hello

This only printed "Hello" once, presumably since the `virt` machine only has one
core, while the SiFive board used in the example has two cores. After printing 
"Hello", the processor sat there running the infinite loop that finished our 
assembly program. Without this infinite loop, the program counter would continue 
incrementing, which could lead it to execute illegal instructions. Or, in more 
relevant security terms, it could start leaking memory.

To terminate Qemu, I pressed `Ctrl+A`, released, then pressed `X`. This sequence 
of keystrokes produced the output:

	QEMU: Terminated

This gives us a process to execute arbitrary RISC-V assembly programs using our 
Qemu emulator. Next step: generate a trace.

### 2022-07-18

Building `riscv-tools` so that we can use `riscv-probe` to "probe control and 
status registers." After several failed attempts, I realized that my `$RISCV` 
environment variable should be set to the directory where my toolchain is 
installed, i.e. `/opt/riscv`. I also noticed that I needed to change some 
`--host` flags in `build.sh` to reflect my installation of the Linux glibc 
toolchain (prefix `riscv64-unknown-linux-gnu-`, rather than the Newlib toolchain 
with prefix `riscv64-unknown-elf-`).

Since I installed my toolchain in a directory that's restricted, I had to use 
the following command to run the build script:

	$ sudo -E ./build.sh

I got a compiler error in `riscv-pk/pk/pk.c`:

	../pk/pk.c: In function 'rest_of_boot_loader':
	../pk/pk.c:139:3: error: both arguments to '__builtin___clear_cache' must be pointers
	  139 |   __clear_cache(0, 0);
		  |   ^~~~~~~~~~~~~~~~~~~
	make: *** [Makefile:319: pk.o] Error 1

The function signature as given by documentation is the following:

	void __builtin___clear_cache(void *begin, void *end);

From the code, I cannot determine what cache is supposed to be cleared here. I 
suppose I *could* try casting the zeroes to `int *` type:

	__clear_cache((int *)0, (int *)0);

# Switching Gears

Let's look into Qemu features that might allow us to look at register values.

## Monitor

The `-monitor` flag lets us view the register contents at a fixed point in time, 
by executing `info registers` in the monitor console. However, I do not believe 
this tool allows us to periodically write register values to a file. Unless, of 
course, I could configure a character device driver that sends monitor info to a
log file. That seems like more trouble than it's worth, for a result that's less 
than optimal.

## gdb (GNU Debugger)

Launching our emulator with the `-s` and `-S` flags makes it listen for an 
incoming TCP connection on port 1234, from gdb, and wait until gdb tells it to 
launch the kernel.

gdb seems to be having trouble connecting to the runtime with our 
assembly program. I'll try connecting it to the runtime with Fedora. 

That also seemed to fail. This might be the fact that I'm in the wrong directory 
to look at the `vmlinux` executable.

	warning: Architecture rejected target-supplied description
	warning: No executable has been specified and target does not support
	determining executable automatically.  Try using the "file" command.
	Truncated register 37 in remote 'g' packet

Everything I've tried creates these error messages.

### 2022-07-19

# riscv-tools

According to an issue report on the GH repo that mentioned the same compile 
error I got, the `riscv-tools` repository is no longer maintained, so I'm going 
to download and compile a new version of `riscv-pk`, the step which keeps 
failing.

	$ git clone https://github.com/riscv-software-src/riscv-pk.git
	$ mkdir build
	$ cd build
	$ ../configure --prefix=$RISCV --host=riscv64-unknown-linux-gnu
	$ make
	$ make install

Config failed on the up-to-date version. Reviewing the log file indicates that 
my version of the riscv-gcc is different than what this package expects.

### 2022-07-20

Not much progress was made today. I worked on creating the Fedora boot demo with
`info registers` accesses, and starting to parse through bits of the QEMU source
to attempt some fprintf hacking.

### 2022-07-21

0) Demo 					*Done!*
1) QEMU sprintf hacking 	*Not close enough for comfort*

For tomorrow
2) QEMU wrapper

# QEMU wrapper

Using the `-S` flag prevents the CPU from starting, and requires a `cont` 
command to proceed with execution. This will be useful to include in my wrapper 
script.

## Other useful monitor commands:

- `stop`:		stops execution of VM
- `c`/`cont`:	resumes execution
- `logfile`:	write logs to the specified file (instead of default)

## Wrapper goals:

1. Start QEMU with a linked ELF as input
	- start the VM paused (`-S`)
	- `-monitor stdio` so program can write commands to monitor
2. Ping monitor every so often (specify as commandline option?)
	- QEMU “single-step” mode (take the first N cycles)
	- build a simple character driver to use instead of `stdio`?
	- write this output to a trace file
3. Terminate VM
	- send `quit` command (or simply `q`) to monitor
		- quit condition?
			- timeout
				-> fixed time?
				-> based on last output change (pc?)
			- user-specified? 
				-> if the program is reading/writing to the 
				   monitor console, does that mean the user can issue a `quit`?
				-> does the user ping the program, or the monitor?

### 2022-07-22

GOAL: Get a Python script that starts QEMU and can write commands to monitor.

## Investigating singlestep

There is a monitor option that runs in "single-step" mode. I have attempted to 
run it on my Hello World program, with no detectable result so far.

	$ qemu-system-riscv64 -machine virt -kernel ~/Desktop/riscv-hello-world/asm/hello -monitor stdio -S
	\[...\]
	(qemu) singlestep
	(qemu) singlestep
	(qemu) info registers
	 pc       0000000000001000
	 \[...\] 
	 f31/ft11 0000000000000000
	(qemu) c

After the `c` command instructing the VM to continue, the entire "Hello" string 
printed in the VM window, and there was no indication that the execution had 
paused for single-step execution.

Looking more deeply at QEMU debugging options, it might be the case that `-d cpu`
will write the CPU registers "after the execution of each code block." This 
could be *very* helpful.

The `-d cpu` option *does* print the same CSRs as monitor shows, but doesn't 
include FPRs. The `-D ./<filename>` flag saves a log in the current directory. 
Thus,

	qemu-system-riscv64 -machine virt -kernel ~/Desktop/riscv-hello-world/asm/hello -monitor stdio -s -S -d cpu -D ./hello_log.txt

produces the log [hello.txt](/hello_log.txt). A similar effect can be achieved with 
`logfile ./hello_log.txt` in the monitor.

### 2022-07-25

# Writing the Python wrapper script

It looks like the subprocess module for Python is the best way to run Qemu 
inside a Python script, as it gives us flexibility of where to route the child 
process's stdin, stdout, and stderr.

That is, assuming I can get it to run Qemu correctly with the flags I need. I've 
gotten `os.system` to function as expected, but am yet to figure out how to do 
the same thing with a subprocess.

Looking at the documentation, I discovered that `subprocess.call("*",shell=True)` 
functions as basically a 1:1 replacement for `os.system`.

### 2022-07-29

# Understanding [Subprocess](https://docs.python.org/3/library/subprocess.html)

After lots of reading and tinkering with the `subprocess` module, I have 
discovered a few things.

	# The following results in undefined behavior when called on the list args
	# but executes as expected when called on args joined into a single string.
	s = sp.run(shlex.join(args), shell=True, text=True, env=env)

The following are equivalent (although they have slightly different return 
values):

	os.system(" ".join(args))
	retcode = sp.call(" ".join(args), shell=True)
	s = sp.run(" ".join(args), shell=True, text=True)

Using `shell=True` leaves a potential vulnerability to shell injection attacks, 
although using `shlex.join()` mitigates this risk by using a properly shell-
escaped command.

It may be necessary/good practice to copy the environment variables into a 
dictionary before opening the subprocess, and passing that dictionary as the 
`env` argument.

`subprocess.run()` waits for the child process to complete before moving on to 
the next line of Python code, however `subprocess.Popen()` "executes a child 
program in a new process." The new `Popen` object can then be sent input from 
the parent and have its output read by the parent.

The child process's `stdin`, `stdout`, and `stderr` can all be sent to an 
existing file object, or through a pipe. For extra flexibility, we will use a 
pipe. `subprocess.PIPE` is a file object that can handle I/O to and from the 
child.

Entering `Ctrl+D` into the terminal without an active process closes the window,
causing a loss of the information that was contained in it.

`Popen.communicate()` waits for the child process to terminate before sending 
and receiving data. I believe I will want to use the `Popen` object's I/O 
streams to send and recieve data.

#### 2022-08-01

1. Troubleshoot concurrency
1. Work QEMU with concurrency know-how
1. Failing that, write a script that runs QEMU with logging enabled, terminates 
QEMU, and parses the output to a Daikon trace.

Subprocess is not the right package to use for spawning interactive programs 
inside Python. See this article about [why you shouldn't use Popen pipes with 
interactive child processes.](https://pexpect.readthedocs.io/en/latest/FAQ.html#whynotpipe)

Instead, we'll use [the `pexpect` package.](https://pexpect.readthedocs.io/en/latest/index.html)

This is ***so*** much easier to work with than `subprocess` was. I *already* 
have [a small QEMU-formatted trace](/src/utils/qtrace_first.txt), after about 20 
minutes of reading and 2 minutes of writing a couple lines of code.

#### 2022-08-02

# Daikon

Daikon takes two files as input: a .decls and a .dtrace:

## Decls file

A .decls containes a header and timepoints.

### Timepoints

Timepoints contain:

- its type
- elements of state (variables)
	- variable kind (variable)
	- declaration and representation type
	- comparability 
		- CSRs, GPRs, and FPRs have their own respective comparabilities.
	- variable name corresponds to register name

Per Calvin's recommendation: declare all variables the same way at 
`tick():::ENTER` and `tick():::EXIT0`. Additionally, give the same values at 
enter and exit.

-> Can we have *no* exit values?


## dtrace files

A .dtrace consists of a bunch of program points.

### Program point

Program points have the following:

- a name, with enter or exit
- a nonce, which is monotonically increasing (1-indexed)
- every register
	- name
	- value
	- the (believed) hardcoded value 1

There must be a line of whitespace between program points, or Daikon will error. 
Extra whitespace might be allowed, but that minimum must be present.

qtrace -> 1 dtrace, 1 decls

# Priorities:

1. Get Daikon working and parse qtraces into dtraces
2. Run Fedora on SiFive emulation and see if it logs different CSRs.
	-> *it doesn't.*

## Writing qToDaikon

This script needs to take a qtrace, preferably *either* a monitor trace *or* a 
QEMU log file, and change it into a dtrace. At the heart of this problem is 
parsing our register values into an internal data structure, such as a list. 
Conveniently, a lot of that can be handled by this one line of code:

	re.findall("\w+\s+[0-9a-f]{16}|\w+\s+[0-9a-f]x[0-9a-f]",line)

This uses a regular expression to match the labels and registers from the qtrace 
format into a list of strings, where each string has a register label/value pair 
that essentially forms a program point. This is something we can quickly comb 
through and write to a dtrace file.

### 2022-08-03

# Installing Daikon

Following the [Daikon install instructions](https://plse.cs.washington.edu/daikon/download/doc/daikon.html#Installing-Daikon),
I unpacked the Daikon distribution, like so:

	$ mkdir ~/Repos/Daikon
	$ cd ~/Repos/Daikon
	$ wget http://plse.cs.washington.edu/daikon/download/daikon-5.8.12.tar.gz
	$ tar zxf daikon-5.8.12.tar.gz

This created a `daikon-5.8.12/` subdirectory. I then executed the following:

	$ export DAIKONDIR=~/Repos/Daikon/daikon-5.8.12
	$ source $DAIKONDIR/scripts/daikon.bashrc

This output the error message:

	Cannot infer JAVA_HOME; please set it.  Aborting daikon.bashrc .

I realized I had to install the Java Development Kit, which I did with the 
following:

	$ sudo apt install default-jdk

and verified installation with:

	$ java -version

Then, I checked that `DAIKONDIR` was still set correctly with `echo`, and I 
repeated the `source` command transcribed above. This no longer returned an 
error message, and I checked that it had set the environment variable 
`JAVA_HOME`, as a sanity check that it had done its work, and sure enough, I got 
the filepath I expected.

# Continuing qToDaikon

While troubleshooting the above and waiting for installations to finish, I wrote 
the parts of `qToDaikon.py` that open a `.dtrace` file for writing, and parse 
the input into a 2D list of timepoints by register name/value strings. Next, we 
have to take this 2D list and parse the strings inside it, then write those 
register names and values into a `.dtrace` file in the proper format.

### 2022-08-04

In our `qscript` output, we notice that we are logging duplicate register values 
at many different timepoints, because we are receiving `info registers` outputs 
more often than the values are actually updated. To find the number of *unique* 
timesteps, we compare the value of every register at the current timepoint to 
the corresponding value at the previous timepoint using list equality. We only 
append a timepoint to the list of timepoints if it passes this uniqueness check.
