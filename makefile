test:
	nose2

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt
