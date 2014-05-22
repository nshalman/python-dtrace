#!/usr/bin/env python

import usdt
import logging

class DtraceLogger(logging.Handler):
	def __init__(self):
		logging.Handler.__init__(self)
		self.provider = usdt.Provider("python", "dtrace-logger")
		self.debug_probe = usdt.Probe("logging", "debug", ["int", "char *"])
		self.info_probe = usdt.Probe("logging", "info", ["int", "char *"])
		self.warning_probe = usdt.Probe("logging", "warning", ["int", "char *"])
		self.error_probe = usdt.Probe("logging", "error", ["int", "char *"])
		self.critical_probe = usdt.Probe("logging", "critical", ["int", "char *"])
		self.notset_probe = usdt.Probe("logging", "notset", ["int", "char *"])
		self.provider.add_probe(self.debug_probe)
		self.provider.add_probe(self.info_probe)
		self.provider.add_probe(self.warning_probe)
		self.provider.add_probe(self.error_probe)
		self.provider.add_probe(self.critical_probe)
		self.provider.add_probe(self.notset_probe)
		self.provider.enable()
	def emit(self, record):
		if record.levelno >= logging.CRITICAL:
			probe = self.critical_probe
		elif record.levelno >= logging.ERROR:
			probe = self.error_probe
		elif record.levelno >= logging.WARNING:
			probe = self.warning_probe
		elif record.levelno >= logging.INFO:
			probe = self.info_probe
		elif record.levelno >= logging.DEBUG:
			probe = self.debug_probe
		else:
			probe = self.notset_probe
		probe.fire([record.levelno, record.msg])

def main():
	pass

if __name__ == "__main__":
	dtrace_handler = DtraceLogger()
	logger = logging.getLogger()
	logger.addHandler(dtrace_handler)
	logger.debug("debug message")
	logger.info("info message")
	logger.warning("warning message")
	logger.error("error message")
	logger.critical("critical message")
	logger.log(0, "notset message")

	logger.setLevel(logging.NOTSET)

	logger.debug("debug message")
	logger.info("info message")
	logger.warning("warning message")
	logger.error("error message")
	logger.critical("critical message")
	logger.log(logging.NOTSET, "notset message")
