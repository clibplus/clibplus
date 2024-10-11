.PHONY: install

install:
	sudo apt update -y && apt upgrade -y
	sudo apt install gcc build-essential -y
	# sudo apt install libssl-dev # Lib For Sockets

build:
	# GC Lib
	gcc -c GC/gc.c
	ar rcs gc.a gc.o; rm gc.o; mv gc.a /usr/local/lib/libgc.a

	# Thread Lib
	gcc -c Thread/thread.c
	ar rcs thread.a thread.o; rm thread.o; mv thread.a /usr/local/lib/libthread.a

	# String Lib
	gcc -c String/string.c
	ar rcs string.a string.o; rm string.o; mv string.a /usr/local/lib/libstring.a

	# Array Lib
	gcc -c Array/array.c
	ar rcs array.a array.o; rm array.o; mv array.a /usr/local/lib/libarray.a

	# Map Lib
	gcc -c Map/map.c
	ar rcs map.a map.o; rm map.o; mv map.a /usr/local/lib/libmap.a

	# OS DIR

	# File Lib
	gcc -c OS/file.c
	ar rcs file.a file.o; rm file.o; mv file.a /usr/local/lib/libfile.a
