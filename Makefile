usdt: usdt.py libusdt.so
	sudo dtrace -Zqn '::hello:{printf("%s:%s:%s:%s %s\n", probeprov, probemod, probefunc, probename, copyinstr(arg0));}' -c ./usdt.py
	sudo dtrace -Z -s test.d -c ./test2.py

libusdt.so: libusdt/libusdt.a
	gcc -g -shared -o $@ -Wl,--whole-archive $<

test: dtrace.so test.py
	sudo dtrace -Zqn ':::testname{printf("%s\n",copyinstr(arg0));}' -c ./test.py

dtrace.so: libusdt/libusdt.a dtrace.c setup.py
	rm -rf dtrace.so build/
	python setup.py build
	mv build/lib*/*.so .

libusdt/libusdt.a:
	git submodule init
	git submodule update
	cd libusdt ; cat /opt/local/etc/pkgin/repositories.conf | sed 's|.*/\([^/]*\)/All/|\1|' | xargs -iARCHY make ARCH=ARCHY clean all

.PHONY: clean

clean:
	git clean -fdX
