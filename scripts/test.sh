#!/bin/sh
set -e

mypy .
pytest --spec -vvvv
