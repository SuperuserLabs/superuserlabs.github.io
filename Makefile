PUG_ROOTS=index.pug thankful/index.pug
PUG_OPTS='{"basedir": "."}'

build:
	pug -O $(PUG_OPTS) $(PUG_ROOTS)

dev-pug:
	pug --watch -O $(PUG_OPTS) $(PUG_ROOTS)

dev-scss:
	npm run scss-watch scss:css

host:
	python -m http.server 8123
