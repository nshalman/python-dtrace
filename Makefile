test: dtrace.so test.py
	@echo
	@echo Run the following in another shell:
	@echo "sudo dtrace -qn ':::testname{printf(\"%s\\\\n\",copyinstr(arg0));}'"
	@echo
	@sleep 2
	python test.py

dtrace.so: libusdt/libusdt.a dtrace.c setup.py
	rm -rf dtrace.so build/
	python setup.py build
	cp build/lib*/dtrace.so .

libusdt/libusdt.a:
	git submodule init
	git submodule update
	cd libusdt ; cat /opt/local/etc/pkgin/repositories.conf | sed 's|.*/\([^/]*\)/All/|\1|' | xargs -iARCHY make ARCH=ARCHY clean all

.PHONY: clean

clean:
	git clean -fdX
