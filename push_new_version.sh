#!/bin/bash
poetry run pytest
[[ ! "$comment" ]] && read -p 'Please set commit comment: ' comment
VERSION=`cat relocation_helper/__init__.py|grep '__version__'||sed -e 's/$/\nprint(__version__)/g'|poetry run python`
git add --all
git commit -m "$VERSION: comment"
