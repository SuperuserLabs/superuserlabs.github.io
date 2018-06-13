.PHONY: install build dev-pug dev-scss host

PUG_OPTS= -O '{"basedir": "."}'

install:
	npm install

build:
	npm run pug -- -o build $(PUG_OPTS) index.pug
	npm run pug -- -o build/thankful $(PUG_OPTS) thankful/index.pug
	npm run sass -- scss/index.scss build/index.css

dev-pug-superuser:
	npm run pug -- -o build --watch $(PUG_OPTS) index.pug

dev-pug-thankful:
	npm run pug -- -o build/thankful --watch $(PUG_OPTS) thankful/index.pug

dev-scss:
	npm run sass -- --watch scss:build

host:
	cd build && python -m http.server 8123
