name:=weighrand


.PHONY: venv
venv:
	python3 -m venv .venv

.PHONY: test
test:
	python3 -m pytest


.PHONY: lint
lint:
	python3 -m pylint $(name) tests *.py


.PHONY: build
build:
	python3 -m build


.PHONY: clean
clean:
	-python3 -m coverage erase
	-pip uninstall $(name)
	find . -depth \( -name '*.pyc' -o -name '__pycache__' -o -name '__pypackages__' \
		-o -name '*.pyd' -o -name '*.pyo' -o -name '*.egg-info' \
		-o -name '*.py,cover'  \) -exec rm -rf \{\} \;
	rm -rf site.py build/ dist/ .tox/ .pytest_cache/
