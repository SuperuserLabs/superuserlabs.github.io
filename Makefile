
build:
	npm run pug index.pug
	npm run sass index.scss index.css

dev-pug:
	npm run pug-watch index.pug

dev-scss:
	npm run scss-watch scss:css

host:
	python -m http.server 8123