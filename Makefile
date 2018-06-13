PUG_ROOTS=index.pug thankful/index.pug
PUG_OPTS='{"basedir": "."}'

install:
	npm install

build:
	npm run pug -O $(PUG_OPTS) $(PUG_ROOTS)

dev-pug:
	npm run pug --watch -O $(PUG_OPTS) $(PUG_ROOTS)

dev-scss:
	npm run scss-watch scss:css

host:
	python -m http.server 8123
