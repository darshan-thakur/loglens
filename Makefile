ENV = .venv
PYTHON = $(ENV)/bin/python

POETRY_ENV = .poetry_venv
POETRY = $(POETRY_ENV)/bin/poetry

$(ENV):
	python3 -m venv $(POETRY_ENV)
	$(POETRY_ENV)/bin/pip install poetry
	$(POETRY_ENV)/bin/poetry config virtualenvs.in-project true

deps: $(ENV)
	$(POETRY) install --no-root

start: deps
	$(PYTHON) -m uvicorn main:app --reload

set_db:
	$(PYTHON) set_db.py

ingest:
	$(PYTHON) ingest_file.py

clean:
	rm -rf $(POETRY_ENV) $(ENV)
	rm poetry.lock