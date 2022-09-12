.PHONY: install build build-dev build-superuser build-thankful dev-pug dev-scss host

PUG_OPTS= -O pugopts.js

install:
	npm install

build: build-superuser build-thankful

build-superuser:
	$(eval DEST := "build-superuser")
	npm run pug -- -o ${DEST} $(PUG_OPTS) index.pug
	npm run pug -- -o ${DEST}/thankful $(PUG_OPTS) thankful
	npm run sass -- scss/index.scss ${DEST}/index.css
	cp -r media ${DEST}/

build-thankful:
	$(eval DEST := "build-thankful")
	mkdir -p ${DEST}
	#echo "getthankful.io" > ${DEST}/CNAME
	npm run pug -- -o ${DEST} $(PUG_OPTS) thankful
	npm run sass -- scss/index.scss ${DEST}/index.css
	cp -r media ${DEST}/

build-dev:
	$(eval DEST := "build-dev")
	DEV=true npm run pug -- -o ${DEST} $(PUG_OPTS) index.pug
	DEV=true npm run pug -- -o ${DEST}/thankful $(PUG_OPTS) thankful
	npm run sass -- scss/index.scss ${DEST}/index.css
	cp -r media ${DEST}/

dev-pug-superuser:
	DEV=true npm run pug -- -o build-dev --watch $(PUG_OPTS) index.pug

dev-pug-thankful:
	DEV=true npm run pug -- -o build-dev/thankful --watch $(PUG_OPTS) thankful/index.pug

dev-scss:
	npm run sass -- --watch scss --output build-dev

serve:
	mkdir -p build-dev
	cp -r media build-dev/
	cd build-dev && python -m http.server 8123

clean:
	rm -rf build
	rm -rf build-dev
	rm -rf build-superuser
	rm -rf build-thankful
