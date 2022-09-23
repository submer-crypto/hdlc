PYTHON = python3
ENVIRONMENT = env

.PHONY: virtual virtual-activate virtual-deactivate requirements-install requirements-freeze lint test docs

virtual: $(ENVIRONMENT)

# Usage: $(make virtual-activate)
virtual-activate: virtual
	@echo source $(ENVIRONMENT)/bin/activate

virtual-deactivate:
	deactivate

requirements-install:
	$(PYTHON) -m pip install -r requirements.txt

requirements-freeze:
	$(PYTHON) -m pip freeze > requirements.txt

lint:
	$(PYTHON) -m flake8 hdlc test

test:
	$(PYTHON) -m pytest -s test

docs:
	sphinx-build -b html docs docs/_build/html

$(ENVIRONMENT):
	$(PYTHON) -m venv $(ENVIRONMENT)
