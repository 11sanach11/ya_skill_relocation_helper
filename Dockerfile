FROM python:3.8.0-slim
WORKDIR /usr/src/app

RUN pip install --no-cache-dir poetry
COPY ./ /tmp/data
RUN cd /tmp/data;rm -rf ./dist ||true;poetry build;pip install ./dist/relocation_helper-*.whl;rm -rf /tmp/data
