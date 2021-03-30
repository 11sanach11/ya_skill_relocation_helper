#!/bin/bash
COMMENT="${1:-}"
VERSION=`cat relocation_helper/__init__.py|grep '__version__'|sed -e 's/$/\nprint(__version__)/g'|poetry run python`
echo "Version: $VERSION"
git tag -l|grep -q "$VERSION" && echo "Version $VERSION already exists, please change version in __init__.py" && exit -1
poetry run pytest
[[ ! "$COMMENT" ]] && read -p 'Please set commit comment: ' COMMENT
git add --all
git commit -m "comment"
git tag -a $VERSION -m "$COMMENT"
git push origin master
git push origin $VERSION
echo "`date`: SUCCESS"
