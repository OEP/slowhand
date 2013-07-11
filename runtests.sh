#!/bin/bash

export SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR/lib"
python3 -m unittest discover -s tests -p test_*.py -v
