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
    int_probe = usdt.Probe("hello", "int", ["char *", "int"])
    test_prov.add_probe(int_probe)
    test_prov.enable()
    for i in range(10):
        hello(1, 2)
    int_probe.fire(["Number Test", 5])
    test_probe.fire(["Hello World"])

if __name__ == "__main__":
    if not usdt.HAVE_USDT:
        usdt.FAKE_DTRACE = True
    main()
