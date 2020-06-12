import sys
from display import *
from draw import *
from script import run

if len(sys.argv) == 3:
  d = int(sys.argv[2].split("-")[1])
  file = sys.argv[1]
  run(file)
elif len(sys.argv) == 2:
    run(sys.argv[1])
elif len(sys.argv) == 1:
    run(input("please enter the filename of an mdl script file: \n"))
else:
    print("Too many arguments.")
