#!/usr/bin/env python

from ctypes import *
import time

_libusdt = cdll.LoadLibrary("./libusdt.so")

usdt_create_provider = _libusdt.usdt_create_provider
usdt_create_provider.argtypes = [c_char_p, c_char_p]

usdt_create_probe = _libusdt.usdt_create_probe
usdt_create_probe.argtypes = [c_char_p, c_char_p, c_int, c_void_p]

usdt_provider_add_probe = _libusdt.usdt_provider_add_probe
usdt_provider_enable = _libusdt.usdt_provider_enable
usdt_fire_probedef = _libusdt.usdt_fire_probedef

class Probe():
	def __init__(self, name, func, arg_desc):
		self.length = len(arg_desc)
		args = (c_char_p * self.length)()
		for i in range(self.length):
			args[i] = arg_desc[i]
		self.probedef = usdt_create_probe(name, func, self.length, args)

	def fire(self, args):
		if len(args) == self.length:
			c_args = (c_void_p * self.length)()
			for i in range(self.length):
				c_args[i] = cast(args[i], c_void_p)
			usdt_fire_probedef(self.probedef, self.length, c_args)

class Provider():
	provider = None
	probes = []
	def __init__(self, provider="python-dtrace", module="default_module"):
		self.provider = usdt_create_provider(provider, module)

	def add_probe(self, probe):
		self.probes.append(probe)
		usdt_provider_add_probe(self.provider, probe.probedef)

	def enable(self):
		usdt_provider_enable(self.provider)

	def __del__(self):
		pass

def main():
	test_prov = Provider("provname", "provmod")
	test_probe = Probe("probename", "func", ["char *"])
	test_prov.add_probe(test_probe)
	test_prov.enable()

	test_probe.fire(["Hello World"])

if __name__ == "__main__":
	main()
