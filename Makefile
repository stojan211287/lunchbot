.PHONY: build dev setup format lint

SHELL := /bin/bash

build: venv requirements.txt
	./venv/bin/pip-sync requirements.txt

dev: venv requirements-dev.txt
	./venv/bin/pip-sync requirements-dev.txt 

format: dev
	./venv/bin/black bot

lint: dev
	./venv/bin/flake8 bot

run: dev
	./venv/bin/python3 -m bot.main

venv: ./venv/
	python3 -m venv venv
	pip3 install --upgrade pip
	./venv/bin/pip3 install pip-tools

requirements.txt: requirements.in
	./venv/bin/pip-compile -o requirements.txt --no-header --no-annotate requirements.in

requirements-dev.txt: requirements-dev.in
	./venv/bin/pip-compile -o requirements-dev.txt --no-header --no-annotate requirements-dev.in
