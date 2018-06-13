.PHONY: install build dev-pug dev-scss host

PUG_OPTS= -O '{"basedir": "."}'

install:
	npm install

build:
	pug -o build $(PUG_OPTS) index.pug
	pug -o build/thankful $(PUG_OPTS) thankful/index.pug

dev-pug-superuser:
	pug --watch $(PUG_OPTS) index.pug

dev-pug-thankful:
	pug --watch $(PUG_OPTS) thankful/index.pug

dev-scss:
	npm run scss-watch scss:css

host:
	cd build && python -m http.server 8123
