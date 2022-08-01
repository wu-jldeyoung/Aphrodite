hello: hello.o link.lds
	riscv64-unknown-linux-gnu-ld -T link.lds -o hello hello.o

hello.o: hello.s
	riscv64-unknown-linux-gnu-as -o hello.o hello.s

clean:
	rm hello hello.o
