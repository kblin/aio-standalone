unit:
	pytest -v

coverage:
	pytest --cov=aiostandalone --cov-report=html --cov-report=term-missing
