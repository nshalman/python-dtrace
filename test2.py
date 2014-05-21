#!/usr/bin/env python

import usdt

@usdt.fbt
def hello(arg1, arg2):
    return True

usdt.enable_fbt()

def main():
    test_prov = usdt.Provider("python", "provmod")
    test_probe = usdt.Probe("hello", "name", ["char *"])
    test_prov.add_probe(test_probe)
    test_prov.enable()
    import time
    for i in range(10):
        hello(1, 2)
    test_probe.fire(["Hello World"])

if __name__ == "__main__":
    if not usdt.HAVE_USDT:
        usdt.FAKE_DTRACE = True
    main()
