test: env/usdt.stamp
	./env/bin/python tests.py || sudo ./env/bin/python tests.py

env/usdt.stamp: env
	env/bin/pip install -r requirements.txt && touch $@

env:
	virtualenv env

.PHONY: clean test

clean:
	rm -rf env
	git clean -fdX
