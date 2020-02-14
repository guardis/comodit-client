#!/bin/bash

set -e

[[ $1 == dev ]] && scripts/build-dev-deb-python2.sh && scripts/build-dev-deb-python3.sh
[[ $1 == prod ]] && scripts/build-deb.sh 

scripts/build-all-deb-withPython3.sh $1
