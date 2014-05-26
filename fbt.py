#!/usr/bin/env python

import functools

import usdt


class fbt(object):
    """
    simple function boundary tracing decorator
    """
    def __init__(self, func):
        self.func = func
        probename = func.__name__
        self.entry_probe = usdt.Probe(probename, "entry", ["char *"])
        self.return_probe = usdt.Probe(probename, "return", ["char *"])
        self.provider = usdt.Provider("python-fbt", "fbt")
        self.provider.add_probe(self.entry_probe)
        self.provider.add_probe(self.return_probe)
        self.provider.enable()

    def __call__(self, *args):
        self.entry_probe.fire([", ".join([str(x) for x in args])])
        ret = self.func(*args)
        self.return_probe.fire([str(ret)])
        return ret

    def __get__(self, obj, objtype):
        """Support instance methods. (http://stackoverflow.com/a/3296318)"""
        return functools.partial(self.__call__, obj)
