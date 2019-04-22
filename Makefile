.PHONY: venv

build: venv requirements.txt
	./venv/bin/pip-sync requirements.txt

lint:
	flake8 bot/

venv: # Create virtualenv with pip-tools
	python3 -m venv venv
	./venv/bin/pip install pip-tools

requirements.txt:
	./venv/bin/pip-compile -o requirements.txt --no-header --no-annotate requirements.in