#!/usr/bin/env python
# Test script
# Author: zlbd

from gimpfu import *

def echo(*args):
  """Print the arguments on standard output"""
  gimp.message(str(args))

register(
  "console_echo", 
  "",
  "",
  "",
  "",
  "",
  "<Toolbox>/Layer/_Test Echo",
  "",
  [
  (PF_STRING, "arg0", "argument 0", "test string"),
  (PF_INT,    "arg1", "argument 1", 100          ),
  (PF_FLOAT,  "arg2", "argument 2", 1.2          ),
  (PF_COLOR,  "arg3", "argument 3", (0, 0, 0)    ),
  ],
  [],
  echo
  )

main()
