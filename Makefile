.PHONY: build dev setup format lint

SHELL := /bin/bash

build: venv requirements.txt
	./venv/bin/pip-sync requirements.txt

dev: venv requirements-dev.txt
	./venv/bin/pip-sync requirements-dev.txt 

deploy: build
	./venv/bin/gunicorn -k uvicorn.workers.UvicornWorker bot.main:app --preload

format: dev
	./venv/bin/black bot

lint: dev
	./venv/bin/flake8 bot

test: dev
	./venv/bin/uvicorn bot.main:app --reload

venv: 
	python3 -m venv venv
	pip3 install --upgrade pip
	./venv/bin/pip3 install pip-tools

requirements.txt: requirements.in
	./venv/bin/pip-compile -o requirements.txt --no-header --no-annotate requirements.in

requirements-dev.txt: requirements-dev.in
	./venv/bin/pip-compile -o requirements-dev.txt --no-header --no-annotate requirements-dev.in
