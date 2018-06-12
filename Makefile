
build:
	pug index.pug

dev:
	pug --watch index.pug

host:
	python -m http.server 8123