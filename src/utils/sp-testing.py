import subprocess as sp
import threading
import signal
import shlex
import time
import os

env = os.environ.copy()

p = sp.Popen("python3", shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, text=True, env=env, universal_newlines=True, bufsize=1)

outs, errs = p.communicate(input="print(\"Hello!\")\n",timeout=20)
print("communicate() output: " + outs)

outs, errs = p.communicate(input="print(\"Hello again!\")\n",timeout=20)
print("communicate() output: " + outs)

p.stdin.write("print(\"write()\")\n")

p.send_signal(signal.SIGINT)

print(p.stdout.read())
