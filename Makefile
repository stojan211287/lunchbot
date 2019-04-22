.PHONY: build dev setup format lint venv requirements.txt requirements-dev.txt

SHELL := /bin/bash

build: venv requirements.txt
	./venv/bin/pip-sync requirements.txt

dev: venv requirements-dev.txt
	./venv/bin/pip-sync requirements-dev.txt

setup: dev
	source ./venv/bin/activate
	black bot
	flake8 bot

format: dev
	black bot

lint: dev
	flake8 bot

venv:
	python3 -m venv venv
	pip install --upgrade pip
	./venv/bin/pip install pip-tools pre-commit
	pre-commit install

requirements.txt:
	./venv/bin/pip-compile -o requirements.txt --no-header --no-annotate requirements.in

requirements-dev.txt:
	./venv/bin/pip-compile -o requirements-dev.txt --no-header --no-annotate requirements-dev.in