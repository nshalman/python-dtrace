#!/usr/sbin/dtrace -s

#pragma D option quiet

:::BEGIN{
printf("logging.d initialized.\n");
}
::logging:
{
printf("%s:%s:%s:%s %d %s\n", probeprov, probemod, probefunc, probename, arg0, copyinstr(arg1));
}
