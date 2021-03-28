#!/bin/bash
docker run --user=`id -u` -m512m --memory-swappiness=0 --ulimit nofile=50:50 \
 -p 53044:53044 -it --rm --name relocation_helper -v /home/chaa/IdeaProjects/relocation-helper/relocation_helper:/usr/src/myapp -w /usr/src/myapp \
  chaa/relocation_helper_poetry python relocation_helper.py
