#!/bin/bash
# Taken from: https://gist.github.com/danielo515/477e130979f76a9d32aa
# Call like this:
#   `LOCAL_DIR=<dir to push> GITHUB_TOKEN=<your password> GITHUB_REF=github.com/<your name>/<your repo>.git ./deploy.sh`
set -e # exit with nonzero exit code if anything fails

# go to the out directory and create a *new* Git repo
cd $LOCAL_DIR
git init

# inside this git repo we'll pretend to be a new user
git config user.name "Travis CI"
git config user.email "<you>@<your-email>"

# The first and only commit to this new Git repo contains all the
# files present with the commit message "Deploy to GitHub Pages".
git add . || echo 'No files added'
git commit -m "Deploy to GitHub Pages" || echo 'No commit made'

# Force push from the current repo's master branch to the remote
# repo's gh-pages branch. (All previous history on the gh-pages branch
# will be lost, since we are overwriting it.) We redirect any output to
# /dev/null to hide any sensitive credential data that might otherwise be exposed.
git push --force --quiet "https://${GITHUB_TOKEN}@${GITHUB_REF}" master:$TARGET_BRANCH #> /dev/null 2>&1
