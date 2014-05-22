#!/usr/sbin/dtrace -s

#pragma D option quiet

::logging:
{
printf("%s:%s:%s:%s %d %s\n", probeprov, probemod, probefunc, probename, arg0, copyinstr(arg1));
}
