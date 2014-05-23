default:
	@echo "try 'make logging' or 'make fbt'"

logging: lib/python2.7/site-packages/usdt
	./helper sudo dtrace -Zs logging.d -c ./usdt_logger.py

fbt: lib/python2.7/site-packages/usdt
	./helper sudo dtrace -Z -s fbt.d -c ./fbt.py

bin/activate:
	virtualenv .

lib/python2.7/site-packages/usdt: bin/activate
	./helper pip install git+git://github.com/nshalman/python-usdt.git


.PHONY: clean

clean:
	rm -rf lib
	git clean -fdX
