.PHONY: all

all: dependencies setup

dependencies:
	sudo apt update -y && apt upgrade -y
	sudo apt install gcc python3 python3-pip -y
	pip install requests

setup:
	cp pkgm.py /bin/
	echo 'alias pm="python3 /bin/pkgm.py"' >> ~/.bashrc
	bash
