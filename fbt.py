#!/usr/bin/env python

import usdt

FBT_PROVIDER = usdt.Provider("python-dtrace", "fbt")


class fbt(object):
    """
    simple function boundary tracing decorator
    """
    def __init__(self, func):
        self.func = func
        probename = func.__name__
        self.entry_probe = usdt.Probe(probename, "entry", ["char *"])
        self.return_probe = usdt.Probe(probename, "return", ["char *"])
        FBT_PROVIDER.add_probe(self.entry_probe)
        FBT_PROVIDER.add_probe(self.return_probe)

    def __call__(self, *args):
        self.entry_probe.fire([", ".join([str(x) for x in args])])
        ret = self.func(*args)
        self.return_probe.fire([str(ret)])
        return ret


def enable_fbt():
    """
    enable the fbt provider,
    must not be called until all decorated functions have been defined
    """
    FBT_PROVIDER.enable()
