.PHONY: examples schemas all test format

CODE_DIRS = scripts/ tests/ trial_balloon/
RUN = poetry run

examples:
	$(RUN) scripts/generate_examples.py

schemas:
	$(RUN) scripts/generate_schemas.py

all: examples schemas

test:
	$(RUN) pytest tests/

format:
	$(RUN) autoflake -ri --ignore-init-module-imports --remove-all-unused-imports $(CODE_DIRS)
	$(RUN) isort $(CODE_DIRS)
	$(RUN) lavender $(CODE_DIRS)

lint:
	$(RUN) flake8 --max-line-length=99 $(CODE_DIRS)
	$(RUN) mypy $(CODE_DIRS)

dist:
	poetry build
