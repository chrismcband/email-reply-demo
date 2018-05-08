#!/bin/bash

DEFAULT_CODE_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../"
CODE_ROOT=${CODE_ROOT:=$DEFAULT_CODE_ROOT}
DEFAULT_VENV="/home/$(whoami)/.virtualenvs/email_reply_demo"
VENV=${VENV:=$DEFAULT_VENV}

cd $CODE_ROOT
source ${VENV}/bin/postactivate
exec ${VENV}/bin/gunicorn -c $CODE_ROOT/config/gunicorn.py config.wsgi