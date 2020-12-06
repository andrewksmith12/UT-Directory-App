test: TestDirectoryLookup.py
	coverage run    --branch TestDirectoryLookup.py >  TestDirectoryLookup.tmp 2>&1
	coverage report -m                      >> TestDirectoryLookup.tmp
	cat TestDirectoryLookup.tmp
