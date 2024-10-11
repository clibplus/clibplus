.PHONY: install

install:
	sudo apt update -y && apt upgrade -y
	sudo apt install gcc -y
	sudo apt install gcc build-essential -y
	# sudo apt install libssl-dev -y # Lib For Sockets

build:
	# GC Lib
	gcc -c GC/gc.c
	ar rcs gc.a gc.o; rm gc.o; mv gc.a /usr/local/lib/libgc.a

	# Thread Lib
	gcc -c Thread/thread.c
	ar rcs thread.a thread.o; rm thread.o; mv thread.a /usr/local/lib/libthread.a

	# str Lib
	gcc -c String/str.c
	ar rcs str.a str.o; rm str.o; mv str.a /usr/local/lib/libstr.a

	# Array Lib
	gcc -c Array/array.c
	ar rcs array.a array.o; rm array.o; mv array.a /usr/local/lib/libarr.a

	# Map Lib
	gcc -c Map/map.c
	ar rcs map.a map.o; rm map.o; mv map.a /usr/local/lib/libmap.a

	# OS DIR

	# File Lib
	gcc -c OS/file.c
	ar rcs file.a file.o; rm file.o; mv file.a /usr/local/lib/libfile.a

setup:
	# Move headers
	mkdir -p /usr/local/include/clibs
	cp -rf String/*.h /usr/local/include/clibs/str.h
	cp -rf Array/*.h /usr/local/include/clibs/arr.h
	cp -rf Map/*.h /usr/local/include/clibs/map.h
	cp -rf GC/*.h /usr/local/include/clibs/gc.h
	cp -rf Thread/*.h /usr/local/include/clibs/thread.h
