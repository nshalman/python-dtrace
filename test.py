#!/usr/bin/env python

import dtrace
import time
import traceback

dtrace.provider("testprov", "testmod")
dtrace.simple_probe("testfunc", "testname")

def wrapper(func):
	def newfunc(*args):
		pad = len(traceback.extract_stack()) * " "
		dtrace.fire(pad + "Entered " + func.__name__)
		ret = func(*args)
		dtrace.fire(pad + "Exited " + func.__name__)
		return ret
	return newfunc

@wrapper
def timeout1():
	return "Hello"

@wrapper
def timeout2():
	return "World"

@wrapper
def timeout3():
	print timeout1() + " " + timeout2()

for i in range(2):
	timeout3()
	dtrace.fire("Hello dtrace")
	time.sleep(1)
