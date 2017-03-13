#/bin/bash

set -e

ENV=env
PIP_CMD=${ENV}/bin/pip

if [ ! -d "$ENV" ]; then
  echo "Creating virtualenv..."
  virtualenv ${ENV}
  ${PIP_CMD} install -U pip
  ${PIP_CMD} install -r requirements.txt
else
  echo "All dependencies have been installed"
fi
