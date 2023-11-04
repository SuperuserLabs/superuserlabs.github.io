install:
	bundle install

serve:
	bundle exec jekyll serve

build:
	bundle exec jekyll build
	touch _site/.nojekyll
