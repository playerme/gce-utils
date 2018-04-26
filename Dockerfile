FROM python:3-alpine

RUN pip install --upgrade pip
RUN pip install pipenv
WORKDIR /gce-utils
ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --system
